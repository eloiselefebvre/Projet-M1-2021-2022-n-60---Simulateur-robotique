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
    COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]

    # MSO TODO : ça serait pratique de mettre la couleur en paramètre, pour qu'on puisse la choisir à la construction, et effectivement choisir une couleur au hasard si non spécifiée
    def __init__(self,x,y,orientation,robotWidth=50,robotHeight=60,distanceBetweenWheels=50,wheelsRadius=10):
        rep=Rectangle(robotWidth,robotHeight,random.choice(self.COLORS),self.DEFAULT_BORDER_RADIUS)
        super().__init__(x,y,orientation,Representation(rep))
        self._leftWheel = Wheel(-distanceBetweenWheels/2+4,0, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._rightWheel = Wheel(distanceBetweenWheels/2-4,0, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftWheel)
        self.addComponent(self._rightWheel)
        self._distanceBetweenWheels = distanceBetweenWheels


    def move(self):
        # vitesse élémentaire
        rightElementarySpeed = self._rightWheel.getRadius() * self._rightWheel.getSpeed() * self._rightWheel.getCW() * config["time_step"] / 60
        leftElementarySpeed = self._leftWheel.getRadius() * self._leftWheel.getSpeed() * self._leftWheel.getCW() * config["time_step"] / 60

        # vitesse moyenne du robot
        averageSpeedRobot = (rightElementarySpeed + leftElementarySpeed) / 2

        # vitesse le long des axes x et y
        Phi = radians(self._orientation + 90)
        dx = averageSpeedRobot * cos(Phi)
        dy = averageSpeedRobot * sin(Phi)

        # vitesse angulaire
        dPhi = - degrees((rightElementarySpeed - leftElementarySpeed)/(2*self._distanceBetweenWheels)) # repère indirect -> signe -

        self._pos.move(self._pos.getX() + dx, self._pos.getY() + dy)
        self._orientation += dPhi

        self._representation.setParameters(self._pos,self._orientation)

    def setLeftWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed):
        self._rightWheel.setSpeed(speed)

    def setLeftWheelCW(self):
        self._leftWheel.cw()

    def setLeftWheelCCW(self):
        self._leftWheel.ccw()

    def setRightWheelCW(self):
        self._rightWheel.cw()

    def setRightWheelCCW(self):
        self._rightWheel.ccw()