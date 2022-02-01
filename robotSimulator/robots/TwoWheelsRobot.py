from math import cos,sin,radians,degrees

from . import Robot
from robotSimulator.representation.shapes import Rectangle
from robotSimulator.representation import Representation
from robotSimulator.actuators import Wheel
from robotSimulator.config import *

import random

class TwoWheelsRobot(Robot):

    DEFAULT_WHEEL_WIDTH = 8
    DEFAULT_BORDER_RADIUS = 3

    def __init__(self,x,y,orientation,color=None,robotWidth=50,robotHeight=60,distanceBetweenWheels=50,wheelsRadius=10):
        rep=Rectangle(robotWidth,robotHeight,color,self.DEFAULT_BORDER_RADIUS)
        super().__init__(x,y,orientation,Representation(rep),color)
        self._leftWheel = Wheel(-distanceBetweenWheels/2+4,0, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._rightWheel = Wheel(distanceBetweenWheels/2-4,0, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftWheel)
        self.addComponent(self._rightWheel)
        self._distanceBetweenWheels = distanceBetweenWheels


    def move(self):
        # vitesse moyenne du robot
        averageSpeedRobot = (self.getRightElementarySpeed() + self.getLeftElementarySpeed()) / 2

        # vitesse le long des axes x et y
        Phi = radians(self._orientation + 90)
        dx = averageSpeedRobot * cos(Phi)
        dy = averageSpeedRobot * sin(Phi)

        # vitesse angulaire
        dPhi = - degrees((self.getRightElementarySpeed() - self.getLeftElementarySpeed())/(2*self._distanceBetweenWheels)) # repère indirect -> signe -

        self._pos.move(self._pos.getX() + dx, self._pos.getY() + dy)
        self._orientation += dPhi

        self._representation.setParameters(self._pos,self._orientation)

    def setLeftWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed):
        self._rightWheel.setSpeed(speed)

    def getRightWheel(self):
        return self._rightWheel

    def getLeftWheel(self):
        return self._leftWheel

    def getRightElementarySpeed(self):
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed() * config["time_step"] / 60

    def getLeftElementarySpeed(self):
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed() * config["time_step"] / 60

    def setWheelY(self,y):
        self._rightWheel.getRepresentation().getOrigin().setY(y)
        self._leftWheel.getRepresentation().getOrigin().setY(y)
