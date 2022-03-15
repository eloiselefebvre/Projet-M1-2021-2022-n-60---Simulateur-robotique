from abc import ABC,abstractmethod
from robotSimulator.Object import Object
from ..Component import Component
from ..Frame import Frame
from ..representation.Representation import Representation
from ..representation.shapes import Rectangle
from ..representation.shapes.Point import Point
from math import cos, pi, sin, radians, degrees
from robotSimulator.config import config

from ..Pose import Pose
from ..sensors import Sensor


class Robot(ABC,Object):

    TRAJECTORY_COLOR = "#F9886A"
    ODOMETRY_COLOR = "#8B86AC"

    NUMBER_STEPS_BEFORE_REFRESH = 30

    def __init__(self,representation):
        super().__init__(representation)
        self._components=[]
        self._sensors_counter=0
        self._actuators_counter=0

        self._acceleration=1 # TODO : Revoir le changement lorsque l'accelaration est initialement définie

        # TRAJECTORY ATTRIBUTES
        self._trajectory = []
        self._trajectoryCounter=0
        self._trajectoryDrawn = False

        # ODOMETRY ATTRIBUTES
        self._odometry = []
        self._odometryCounter=0
        self._odometryDrawn=False
        self._odometryPose=None

    def addComponent(self,comp,x=0,y=0,orientation=0):
        if isinstance(comp,Component):
            pose=Pose(x,y,orientation)
            comp.setPose(pose)
            comp.setParent(self)
            comp.getFrame().setBaseFrame(self._frame)
            comp.getFrame().setCoordinates(pose)
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    def move(self):
        self.updateTrajectory()
        self.updateOdometry()
        self.notifyObservers("stateChanged")

    def getComponents(self):
        return self._components

    @abstractmethod
    def getLeftLinearSpeed(self):
        pass

    @abstractmethod
    def getRightLinearSpeed(self):
        pass

    @abstractmethod
    def getDistanceBetweenWheels(self):
        pass

    def accelerationChanged(self,sender):
        self._acceleration=sender.getAcceleration()

    # TRAJECTORY METHODS
    def updateTrajectory(self):
        if self._trajectoryCounter==0:
            point = Object(Representation(Point(int(self._pose.getX()), int(self._pose.getY()),self.TRAJECTORY_COLOR)))
            self._trajectory.append(point)
            if self._trajectoryDrawn:
                self._env.addVirtualObject(self._trajectory[-1])
        self._trajectoryCounter=(self._trajectoryCounter+1)%self.NUMBER_STEPS_BEFORE_REFRESH

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

    def getTrajectoryDrawn(self):
        return self._trajectoryDrawn

    def toggleTrajectoryDrawn(self):
        self._trajectoryDrawn = not self._trajectoryDrawn

    # ODOMETRY METHODS
    def updateOdometry(self):
        vd = self.getRightLinearSpeed()
        vg = self.getLeftLinearSpeed()
        v = (vd + vg) / 2
        e = self.getDistanceBetweenWheels()
        d = v * config["time_step"] / 60

        x=self._odometryPose.getX()
        y=self._odometryPose.getY()
        if vd != vg:
            R = e * (vd + vg) / (vd - vg)
            if R != 0:
                # calcul des paramètres du cercle trajectoire
                x0 = x + R * cos(-radians(self._odometryPose.getOrientation()))
                y0 = y + R * sin(-radians(self._odometryPose.getOrientation()))
                # calcul position du robot
                d_teta = d / R
                self._odometryPose.rotate(degrees(d_teta))
                self._odometryPose.move(x0 - R * cos(-radians(self._odometryPose.getOrientation())),
                                        y0 - R * sin(-radians(self._odometryPose.getOrientation())))

        else:
            nx=x-d * sin(-radians(self._odometryPose.getOrientation()))
            ny=y+d * cos(-radians(self._odometryPose.getOrientation()))
            self._odometryPose.move(nx,ny)

        if self._odometryCounter == 0:
            point = Object(Representation(Point(int(self._odometryPose.getX()), int(self._odometryPose.getY()), self.ODOMETRY_COLOR)))
            self._odometry.append(point)
            if self._odometryDrawn:
                self._env.addVirtualObject(self._odometry[-1])
        self._odometryCounter = (self._odometryCounter + 1) % self.NUMBER_STEPS_BEFORE_REFRESH

    def showOdometry(self):
        for point in self._odometry:
            self._env.addVirtualObject(point)

    def hideOdometry(self):
        for point in self._odometry:
            self._env.removeVirtualObject(point)

    def deleteOdometry(self):
        self.hideOdometry()
        self._odometry.clear()

    def toggleOdometryDrawn(self):
        self._odometryDrawn=not self._odometryDrawn

    def getOdometryDrawn(self):
        return self._odometryDrawn

    def setOdometryPose(self,pose):
        # self.deleteOdometry()
        self._odometryPose=pose
        self._odometryPose.setOrientation(-self._odometryPose.getOrientation())

    def getOdometryPose(self):
        return self._odometryPose
