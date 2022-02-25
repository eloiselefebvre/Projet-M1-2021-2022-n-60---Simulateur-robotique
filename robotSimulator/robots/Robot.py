from abc import ABC, abstractmethod

from robotSimulator import Object
from ..Component import Component
from ..representation import Representation
from ..representation.shapes import Point
from ..sensors.Sensor import Sensor
from ..Pose import Pose

class Robot(ABC,Object):

    TRAJECTORY_COLOR = "#F9886A"

    def __init__(self,representation):
        super().__init__(representation)
        self._components=[]
        self._sensors_counter=0
        self._actuators_counter=0
        self._drawTrajectory=False

    def addComponent(self,comp,x=0,y=0,orientation=0):
        if isinstance(comp,Component):
            comp.setPose(Pose(x,y,orientation))
            comp.setParent(self)
            if comp.getID() == comp.generateDefaultID():
                if isinstance(comp,Sensor):
                    self._sensors_counter += 1
                    comp.completeID(self._sensors_counter)
                else:
                    self._actuators_counter += 1
                    comp.completeID(self._actuators_counter)
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    def move(self):
        self.drawTrajectory()
        for comp in self._components:
            if hasattr(comp,"refresh"):
                comp.refresh()

    def getComponents(self):
        return self._components

    def drawTrajectory(self):
        if self._drawTrajectory==True:
            point = Object(Representation(Point(int(self._pose.getX()), int(self._pose.getY()),self.TRAJECTORY_COLOR)))
            self._env.addVirtualObject(point)

