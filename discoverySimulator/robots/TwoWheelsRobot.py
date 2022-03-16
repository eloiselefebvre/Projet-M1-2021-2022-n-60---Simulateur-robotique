from math import cos,sin,radians,degrees

from . import Robot
from discoverySimulator.representation.shapes.Rectangle import Rectangle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.actuators.Wheel import Wheel
from discoverySimulator.config import config

import random

class TwoWheelsRobot(Robot):

    DEFAULT_WHEEL_WIDTH = 8
    DEFAULT_BORDER_RADIUS = 3
    COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]

    def __init__(self,color=None,robotWidth=50,robotHeight=60,distanceBetweenWheels=50,wheelsRadius=10,wheelYPos=0):
        self._color = random.choice(self.COLORS) if color is None else color
        rep=Rectangle(robotWidth,robotHeight,self._color,self.DEFAULT_BORDER_RADIUS)
        rep.addOrientationMark()
        super().__init__(Representation(rep))
        self._leftWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._rightWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftWheel,(-distanceBetweenWheels+self.DEFAULT_WHEEL_WIDTH)/2,wheelYPos)
        self.addComponent(self._rightWheel,(distanceBetweenWheels-self.DEFAULT_WHEEL_WIDTH)/2,wheelYPos)
        self._distanceBetweenWheels = distanceBetweenWheels
        self._leftWheel.setID("LeftWheel")
        self._rightWheel.setID("RightWheel")


    def move(self):
        if not self._isCollided:
            # vitesse moyenne du robot
            averageSpeedRobot = (self.getRightElementarySpeed() + self.getLeftElementarySpeed()) / 2

            # vitesse le long des axes x et y
            Phi = radians(self._pose.getOrientation() + 90)
            dx = averageSpeedRobot * cos(Phi)
            dy = averageSpeedRobot * sin(Phi)

            # vitesse angulaire
            dPhi = degrees(-(self.getRightElementarySpeed() - self.getLeftElementarySpeed())/(2*self._distanceBetweenWheels)) # repère indirect -> signe -

            self.setRotCenter()
            self._pose.move(self._pose.getX() + dx, self._pose.getY() + dy)
            self._pose.rotate(dPhi)

            self.isCollided()

        super().move()

    def getAverageSpeed(self):
        averageSpeedRobot = (self.getRightElementarySpeed() + self.getLeftElementarySpeed()) / 2
        return averageSpeedRobot

    def setRotCenter(self):
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX()) / 2,
                                     (self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY()) / 2)

    def setLeftWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed):
        self._rightWheel.setSpeed(speed)

    def getRightWheel(self):
        return self._rightWheel

    def getLeftWheel(self):
        return self._leftWheel

    def getRightLinearSpeed(self):
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed()

    def getRightElementarySpeed(self):
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed()*config["update_time_step"] / 60 * self._acceleration

    def getLeftLinearSpeed(self):
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed()

    def getLeftElementarySpeed(self):
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed() * config["update_time_step"] / 60 * self._acceleration

    def setWheelY(self,y):
        self._rightWheel.getRepresentation().getOrigin().setY(y)
        self._leftWheel.getRepresentation().getOrigin().setY(y)

    def getDistanceBetweenWheels(self):
        return self._distanceBetweenWheels
