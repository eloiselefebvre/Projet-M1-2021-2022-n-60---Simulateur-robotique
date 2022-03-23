from abc import ABC,abstractmethod

from .. import Object
from ..Component import Component
from ..representation.Representation import Representation
from ..representation.shapes.Point import Point
from math import cos, sin, radians, degrees, atan
from discoverySimulator.config import config, colors
from ..Pose import Pose

class Robot(ABC,Object):

    NUMBER_STEPS_BEFORE_REFRESH = 30

    def __init__(self,representation):
        """
        This method is used to create a new robot
        :param representation: representation of the robot
        """
        super().__init__(representation)
        self._components=[]
        self._sensors_counter=0
        self._actuators_counter=0

        # TRAJECTORY ATTRIBUTES
        self._trajectory = []
        self._trajectoryCounter=0
        self._trajectoryDrawn = False

        # ODOMETRY ATTRIBUTES
        self._odometry = []
        self._odometryCounter=0
        self._odometryDrawn=False
        self._odometryPose=None

        self._pathFollowing=None
        self._isSpeedLocked=False

    def addComponent(self, component, x=0, y=0, orientation=0):
        """
        This method is used to add a component of a robot
        :param component: component to add to the robot
        :param x: x coordinate of the component on the robot [px]
        :param y: y coordinate of the component on the robot [px]
        :param orientation: orientation of the component on the robot [degrees]
        """
        if isinstance(component, Component):
            pose=Pose(x,y,orientation)
            component.setPose(pose)
            component.setParent(self)
            component.getFrame().setBaseFrame(self._frame)
            component.getFrame().setCoordinates(pose)
            self._components.append(component)
            self._representation.addSubRepresentation(component.getRepresentation())

    def move(self):
        self.updateTrajectory()
        self.updateOdometry()
        self.notifyObservers("stateChanged")

        if self._pathFollowing is not None:
            self._pathFollowing.followPath()

    def getComponents(self):
        """
        This method allows to get all components
        :return: all components
        """
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

    # TRAJECTORY METHODS
    def updateTrajectory(self):
        if self._trajectoryCounter==0:
            point = Object(Representation(Point(colors['trajectory'])))
            self._trajectory.append(point)
            if self._trajectoryDrawn:
                self._environnement.addVirtualObject(self._trajectory[-1], self._pose.getX(), self._pose.getY())
            else:
                self._trajectory[-1].setPose(Pose(self._pose.getX(),self._pose.getY()))
        self._trajectoryCounter=(self._trajectoryCounter+1)%self.NUMBER_STEPS_BEFORE_REFRESH

    def showTrajectory(self):
        for point in self._trajectory:
            point_pose=point.getPose()
            self._environnement.addVirtualObject(point, point_pose.getX(), point_pose.getY())

    def hideTrajectory(self):
        for point in self._trajectory:
            self._environnement.removeVirtualObject(point)
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
        d = v * config["real_update_time_step"]*self._acceleration/60

        x=self._odometryPose.getX()
        y=self._odometryPose.getY()

        if vd != vg and vd!=-vg: # le robot n'avance pas tout droit et ne tourne pas sur place
            R = e * (vd + vg) / (vd - vg)
            # calcul des coordonnées du centre du cercle trajectoire
            x0 = x - R * cos(radians(self._odometryPose.getOrientation()))
            y0 = y - R * sin(radians(self._odometryPose.getOrientation()))

            # calcul position du robot
            dTheta = d / R
            self._odometryPose.rotate(degrees(dTheta))
            self._odometryPose.move(x0 + R * cos(radians(self._odometryPose.getOrientation())),
                                    y0 + R * sin(radians(self._odometryPose.getOrientation())))
        elif vd==-vg: # robot tourne sur place
            dd=vd * config["real_update_time_step"]*self._acceleration/60
            dTheta=atan(dd/e)
            self._odometryPose.rotate(degrees(dTheta))
        else: # robot en ligne droite
            nx=x-d * sin(radians(self._odometryPose.getOrientation()))
            ny=y+d * cos(radians(self._odometryPose.getOrientation()))
            self._odometryPose.move(nx,ny)

        if self._odometryCounter == 0:
            point = Object(Representation(Point(colors['odometry'])))
            self._odometry.append(point)
            if self._odometryDrawn:
                self._environnement.addVirtualObject(self._odometry[-1], self._odometryPose.getX(), self._odometryPose.getY())
            else:
                self._odometry[-1].setPose(Pose(self._odometryPose.getX(), self._odometryPose.getY()))
        self._odometryCounter = (self._odometryCounter + 1) % self.NUMBER_STEPS_BEFORE_REFRESH

    def showOdometry(self):
        for point in self._odometry:
            point_pose = point.getPose()
            self._environnement.addVirtualObject(point, point_pose.getX(), point_pose.getY())

    def hideOdometry(self):
        for point in self._odometry:
            self._environnement.removeVirtualObject(point)

    def deleteOdometry(self):
        self.hideOdometry()
        self._odometry.clear()

    def toggleOdometryDrawn(self):
        self._odometryDrawn=not self._odometryDrawn

    def getOdometryDrawn(self):
        return self._odometryDrawn

    def setOdometryPose(self,pose):
        self._odometryPose=pose

    def getOdometryPose(self):
        return self._odometryPose

    def setPathFollowing(self,pathFollowing):
        self._pathFollowing=pathFollowing

    def setSpeedLock(self,state:bool):
        self._isSpeedLocked=state

    def getBoundingWidth(self):
        return self.getRepresentation().getShape().getBoundingBox().getWidth()

    def getBoundingHeight(self):
        return self.getRepresentation().getShape().getBoundingBox().getHeigt()