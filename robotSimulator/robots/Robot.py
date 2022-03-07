from abc import ABC
from robotSimulator.Object import Object
from ..Component import Component
from ..Odometry import Odometry
from ..representation.Representation import Representation
from ..representation.shapes.Point import Point

from ..Pose import Pose
from ..sensors import Sensor


class Robot(ABC,Object):

    TRAJECTORY_COLOR = "#F9886A"

    def __init__(self,representation):
        super().__init__(representation)
        self._components=[]
        self._sensors_counter=0
        self._actuators_counter=0
        self._drawTrajectory=False
        self._trajectory = []
        self._counter=0
        self._drawOdometry=True #False
        self._odometry = None

    def addComponent(self,comp,x=0,y=0,orientation=0):
        if isinstance(comp,Component):
            comp.setPose(Pose(x,y,orientation))
            comp.setParent(self)
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    def move(self):
        self.updateTrajectory()
        self._odometry.odometry()
        self.notifyObservers("poseChanged")

    def getComponents(self):
        return self._components

    def addOdometry(self):
        self._odometry = Odometry(self,self._env)

    def getOdometry(self):
        return self._odometry

    def getDrawOdometry(self):
        return self._drawOdometry

    def updateTrajectory(self):
        if self._counter==0:
            point = Object(Representation(Point(int(self._pose.getX()), int(self._pose.getY()),self.TRAJECTORY_COLOR)))
            self._trajectory.append(point)
            if self._drawTrajectory:
                self._env.addVirtualObject(self._trajectory[-1])
        self._counter=(self._counter+1)%10

    def getDrawTrajectory(self):
        return self._drawTrajectory

    def setDrawTrajectory(self):
        self._drawTrajectory = not self._drawTrajectory

    def setDrawOdometry(self):
        self._drawOdometry = not self._drawOdometry

    def showTrajectory(self):
        for point in self._trajectory:
            self._env.addVirtualObject(point)

    def hideTrajectory(self):
        for point in self._trajectory:
            self._env.removeVirtualObject(point)
        self._drawTrajectory=False

    def deleteTrajectory(self):
        self.hideTrajectory()
        self._trajectory.clear()

