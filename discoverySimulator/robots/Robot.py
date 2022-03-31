import random
from abc import ABC,abstractmethod
from typing import List

from .. import Object
from ..Component import Component
from ..actuators import Wheel
from ..representation.Representation import Representation
from ..representation.shapes.Point import Point
from math import cos, sin, radians, degrees, atan
from discoverySimulator.config import config, colors
from ..Pose import Pose
from ..sensors import Sensor


class Robot(ABC,Object):

    """ The Robot class provides a robot."""

    __NUMBER_CALLS_BEFORE_REFRESH = 30

    def __init__(self,representation):
        """ Constructs a new robot.
        @param representation Representation of the robot
        """
        super().__init__(representation)
        self._components=[]
        self._sensors_counter=0
        self._actuators_counter=0
        self._wheels=[]

        # TRAJECTORY ATTRIBUTES
        self.__trajectory = []
        self.__trajectoryCounter=0
        self.__trajectoryDrawn = False

        # ODOMETRY ATTRIBUTES
        self.__odometryEnabled=False

        self._pathFollowing=None
        self._isSpeedLocked=False


    # SETTERS
    def setPose(self,pose:Pose):
        super().setPose(pose)
        self.setOdometryPose(pose.copy())
        self._frame.setCoordinates(self._pose)
        self.computeRotationCenter()

    def setOdometryPose(self, pose:Pose):
        self.__odometryPose = pose

    def setPathFollowing(self, pathFollowing):
        self._pathFollowing = pathFollowing

    def setSpeedLock(self, state: bool):
        self._isSpeedLocked = state

    # GETTERS
    def getComponents(self) -> List[Component]:
        """ Returns all components.
        @return All components of the robot
        """
        return self._components

    @abstractmethod
    def getLeftLinearSpeed(self) -> float:
        """ Returns the left linear speed.
        @return  The left linear speed
        """
        pass

    @abstractmethod
    def getRightLinearSpeed(self) -> float:
        """ Returns the right linear speed.
        @return  The right linear speed
        """
        pass

    @abstractmethod
    def getDistanceBetweenWheels(self) -> float:
        """ Returns the distance between wheels.
        @return  The distance between wheels
        """
        pass

    def getTrajectoryDrawn(self) -> bool:
        return self.__trajectoryDrawn

    def getOdometryDrawn(self) -> bool:
        return self.__odometryDrawn

    def getOdometryPose(self) -> Pose:
        return self.__odometryPose

    def getWheels(self) -> List[Wheel]:
        """ Returns all the wheels of a robot.
        @return  All the wheels of the robot
        """
        return self._wheels

    def getBoundingWidth(self) -> float:
        return self.getRepresentation().getShape().getBoundingBox().getWidth()

    def getBoundingHeight(self) -> float:
        return self.getRepresentation().getShape().getBoundingBox().getHeigt()

    def addComponent(self, component:Component, x:float=0, y:float=0, orientation:float=0):
        """ Adds a component of a robot.
        @param component: component to add to the robot
        @param x  x coordinate of the component on the robot [px]
        @param y  y coordinate of the component on the robot [px]
        @param orientation  orientation of the component on the robot [degrees]
        """
        if isinstance(component, Component):
            pose=Pose(-x,y,orientation)
            component.setPose(pose)
            component.setParent(self)
            component.getFrame().setBaseFrame(self._frame)
            component.getFrame().setCoordinates(pose)
            if self._environment is not None:
                component.setEnvironnement(self._environment)
                if isinstance(component,Sensor):
                    self._environment.addSensor(component)

            self._components.append(component)
            if isinstance(component,Wheel):
                self._wheels.append(component)
            self._representation.addSubRepresentation(component.getRepresentation())

    def move(self):
        self.__updateTrajectory()
        self.__updateOdometry()
        self.notifyObservers("stateChanged")

        if self._pathFollowing is not None:
            self._pathFollowing.followPath()

    # TRAJECTORY METHODS
    def __updateTrajectory(self):
        if self.__trajectoryCounter==0:
            point = Object(Representation(Point(colors['trajectory'])))
            self.__trajectory.append(point)
            if self.__trajectoryDrawn:
                self._environment.addVirtualObject(self.__trajectory[-1], self._pose.getX(), self._pose.getY())
            else:
                self.__trajectory[-1].setPose(Pose(self._pose.getX(), self._pose.getY()))
        self.__trajectoryCounter= (self.__trajectoryCounter + 1) % self.__NUMBER_CALLS_BEFORE_REFRESH

    def __showTrajectory(self):
        # Shows the trajectory of a robot.
        for point in self.__trajectory:
            point_pose=point.getPose()
            self._environment.addVirtualObject(point, point_pose.getX(), point_pose.getY())

    def __hideTrajectory(self):
        # Hides the trajectory of a robot.
        for point in self.__trajectory:
            self._environment.removeVirtualObject(point)
        self._drawTrajectory=False

    def deleteTrajectory(self):
        self.__hideTrajectory()
        self.__trajectory.clear()
        self.__trajectoryCounter=0

    def toggleTrajectoryDrawn(self):
        self.__trajectoryDrawn = not self.__trajectoryDrawn
        if self.__trajectoryDrawn:
            self.__showTrajectory()
            return
        self.__hideTrajectory()

    # ODOMETRY METHODS
    def isOdometryEnabled(self):
        return self.__odometryEnabled

    def enableOdometry(self,accuracy=1):
        if not self.__odometryEnabled:
            self.__odometryEnabled=True
            self.__odometry = []
            self.__odometryCounter = 0
            self.__odometryDrawn = False
            self.__odometryPose=None
            self.__odometryNoise=1-(accuracy if 0<=accuracy<=1 else 1)
            if self._pose is not None:
                self.__odometryPose=self._pose.copy()

    def disableOdometry(self):
        if self.__odometryEnabled:
            self.__odometryEnabled=False
            self.__odometryPose=None
            self.deleteOdometry()

    def __updateOdometry(self):
        if self.__odometryEnabled:
            vd = self.getRightLinearSpeed()
            vg = self.getLeftLinearSpeed()

            if self._environment.isReal():
                vd+=random.uniform(-self.__odometryNoise*vd,self.__odometryNoise*vd)
                vg+=random.uniform(-self.__odometryNoise*vg,self.__odometryNoise*vg)

            v = (vd + vg) / 2
            e = self.getDistanceBetweenWheels()
            d = v * config["real_update_time_step"]*self._acceleration/60

            x=self.__odometryPose.getX()
            y=self.__odometryPose.getY()

            if vd != vg and vd!=-vg: # le robot n'avance pas tout droit et ne tourne pas sur place
                R = e * (vd + vg) / (vd - vg)
                # calcul des coordonnées du centre du cercle trajectoire
                x0 = x - R * cos(radians(self.__odometryPose.getOrientation()))
                y0 = y - R * sin(radians(self.__odometryPose.getOrientation()))

                # calcul position du robot
                dTheta = d / R
                self.__odometryPose.rotate(degrees(dTheta))
                self.__odometryPose.move(x0 + R * cos(radians(self.__odometryPose.getOrientation())),
                                         y0 + R * sin(radians(self.__odometryPose.getOrientation())))
            elif vd==-vg: # robot tourne sur place
                dd=vd * config["real_update_time_step"]*self._acceleration/60
                dTheta=atan(dd/e)
                self.__odometryPose.rotate(degrees(dTheta))
            else: # robot en ligne droite
                nx=x-d * sin(radians(self.__odometryPose.getOrientation()))
                ny=y+d * cos(radians(self.__odometryPose.getOrientation()))
                self.__odometryPose.move(nx, ny)

            if self.__odometryCounter == 0:
                point = Object(Representation(Point(colors['odometry'])))
                self.__odometry.append(point)
                if self.__odometryDrawn:
                    self._environment.addVirtualObject(self.__odometry[-1], self.__odometryPose.getX(), self.__odometryPose.getY())
                else:
                    self.__odometry[-1].setPose(Pose(self.__odometryPose.getX(), self.__odometryPose.getY()))
            self.__odometryCounter = (self.__odometryCounter + 1) % self.__NUMBER_CALLS_BEFORE_REFRESH

    def __showOdometry(self):
        if self.__odometryEnabled:
            for point in self.__odometry:
                point_pose = point.getPose()
                self._environment.addVirtualObject(point, point_pose.getX(), point_pose.getY())

    def __hideOdometry(self):
        if self.__odometryEnabled:
            for point in self.__odometry:
                self._environment.removeVirtualObject(point)

    def deleteOdometry(self):
        if self.__odometryEnabled:
            self.__hideOdometry()
            self.__odometry.clear()
            self.__odometryCounter=0

    def toggleOdometryDrawn(self):
        self.__odometryDrawn=not self.__odometryDrawn
        if self.__odometryDrawn:
            self.__showOdometry()
            return
        self.__hideOdometry()

    @abstractmethod
    def computeRotationCenter(self):
        pass
