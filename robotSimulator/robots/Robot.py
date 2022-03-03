from abc import ABC, abstractmethod

from robotSimulator import Object
from ..Component import Component

from ..representation import Representation
from ..representation.shapes import Point
from ..sensors.Sensor import Sensor
from ..Pose import Pose

# TODO : Pb point restant lorsque l'on cache la trajectoire

class Robot(ABC,Object):

    TRAJECTORY_COLOR = "#F9886A"

    def __init__(self,representation):
        super().__init__(representation)
        self._components=[]
        self._sensors_counter=0
        self._actuators_counter=0
        self._drawTrajectory=False
        self._trajectory = []

    def addComponent(self,comp,x=0,y=0,orientation=0):
        if isinstance(comp,Component):
            comp.setPose(Pose(x,y,orientation))
            comp.setParent(self)
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    def move(self):
        self.updateTrajectory()
        for comp in self._components:
            if hasattr(comp,"refresh"):
                comp.refresh()
        self.notifyObservers("poseChanged")

    def getComponents(self):
        return self._components

    def updateTrajectory(self):
        point = Object(Representation(Point(int(self._pose.getX()), int(self._pose.getY()),self.TRAJECTORY_COLOR)))
        self._trajectory.append(point)
        if self._drawTrajectory:
            self._env.addVirtualObject(self._trajectory[-1])

    def getDrawTrajectory(self):
        return self._drawTrajectory

    def setDrawTrajectory(self):
        self._drawTrajectory = not self._drawTrajectory

    def showTrajectory(self):
        for point in self._trajectory:
            self._env.addVirtualObject(point)

    def hideTrajectory(self): # TODO : Hide trajectory when robot is not visible
        for point in self._trajectory:
            self._env.removeVirtualObject(point)

    def deleteTrajectory(self):
        self.hideTrajectory()
        self._trajectory.clear()