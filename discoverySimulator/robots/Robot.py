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

class Robot(ABC,Object):

    __NUMBER_CALLS_BEFORE_REFRESH = 30

    # TODO : Noise plus global, ajouter imperfection sur le modèle de la simulation

    def __init__(self,representation):
        """ This method is used to create a new robot
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
        self.__odometry = []
        self.__odometryCounter=0
        self.__odometryDrawn=False
        self.__odometryPose=None

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
        """ This method allows to get all components
        @return All components of the robot
        """
        return self._components

    @abstractmethod
    def getLeftLinearSpeed(self) -> float:
        """ This method is used to get the left linear speed
        @return  The left linear speed
        """
        pass

    @abstractmethod
    def getRightLinearSpeed(self) -> float:
        """ This method is used to get the right linear speed
        @return  The right linear speed
        """
        pass

    @abstractmethod
    def getDistanceBetweenWheels(self) -> float:
        """ This method is used to get distance between wheels
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
        """ This method is used to get all the wheels of a robot
        @return  All the wheels of the robot
        """
        return self._wheels

    def getBoundingWidth(self) -> float:
        return self.getRepresentation().getShape().getBoundingBox().getWidth()

    def getBoundingHeight(self) -> float:
        return self.getRepresentation().getShape().getBoundingBox().getHeigt()

    def addComponent(self, component:Component, x:float=0, y:float=0, orientation:float=0):
        """ This method is used to add a component of a robot.
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

            self._components.append(component)
            if isinstance(component,Wheel):
                self._wheels.append(component)
            self._representation.addSubRepresentation(component.getRepresentation())

    def move(self):
        self.updateTrajectory()
        self.updateOdometry()
        self.notifyObservers("stateChanged")

        if self._pathFollowing is not None:
            self._pathFollowing.followPath()

    # TRAJECTORY METHODS
    def updateTrajectory(self):
        if self.__trajectoryCounter==0:
            point = Object(Representation(Point(colors['trajectory'])))
            self.__trajectory.append(point)
            if self.__trajectoryDrawn:
                self._environnement.addVirtualObject(self.__trajectory[-1], self._pose.getX(), self._pose.getY())
            else:
                self.__trajectory[-1].setPose(Pose(self._pose.getX(), self._pose.getY()))
        self.__trajectoryCounter= (self.__trajectoryCounter + 1) % self.__NUMBER_CALLS_BEFORE_REFRESH

    # TODO : Revoir le système et la bascule de drawTrajectory
    def showTrajectory(self):
        """ This method is used to show the trajectory of a robot
        """
        for point in self.__trajectory:
            point_pose=point.getPose()
            self._environnement.addVirtualObject(point, point_pose.getX(), point_pose.getY())

    def hideTrajectory(self):
        """ This method is used to hide the trajectory of a robot
        """
        for point in self.__trajectory:
            self._environnement.removeVirtualObject(point)
        self._drawTrajectory=False

    def deleteTrajectory(self):
        self.hideTrajectory()
        self.__trajectory.clear()

    def toggleTrajectoryDrawn(self):
        self.__trajectoryDrawn = not self.__trajectoryDrawn

    # ODOMETRY METHODS
    def updateOdometry(self):
        vd = self.getRightLinearSpeed()
        vg = self.getLeftLinearSpeed()

        if self._environnement.isReal():
            vd+=random.uniform(-self._environnement.getNoiseStrengh()*vd,self._environnement.getNoiseStrengh()*vd)
            vg+=random.uniform(-self._environnement.getNoiseStrengh()*vg,self._environnement.getNoiseStrengh()*vg)

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
                self._environnement.addVirtualObject(self.__odometry[-1], self.__odometryPose.getX(), self.__odometryPose.getY())
            else:
                self.__odometry[-1].setPose(Pose(self.__odometryPose.getX(), self.__odometryPose.getY()))
        self.__odometryCounter = (self.__odometryCounter + 1) % self.__NUMBER_CALLS_BEFORE_REFRESH

    def showOdometry(self):
        """ This method is used to show the odometry of a robot
        """
        for point in self.__odometry:
            point_pose = point.getPose()
            self._environnement.addVirtualObject(point, point_pose.getX(), point_pose.getY())

    def hideOdometry(self):
        """ This method is used to hide the odometry of a robot
        """
        for point in self.__odometry:
            self._environnement.removeVirtualObject(point)

    def deleteOdometry(self):
        self.hideOdometry()
        self.__odometry.clear()

    def toggleOdometryDrawn(self):
        self.__odometryDrawn=not self.__odometryDrawn

    @abstractmethod
    def computeRotationCenter(self):
        pass
