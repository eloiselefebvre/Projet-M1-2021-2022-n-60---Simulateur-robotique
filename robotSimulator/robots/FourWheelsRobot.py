from . import Robot
from robotSimulator.representation.shapes import Rectangle
from robotSimulator.representation import Representation
from robotSimulator.actuators import Wheel
import random
from math import cos,sin,radians,degrees

from robotSimulator.config import *

class FourWheelsRobot(Robot):

    DEFAULT_WHEEL_WIDTH = 8
    DEFAULT_BORDER_RADIUS = 3
    COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]

    def __init__(self, x, y, orientation, robotWidth=50, robotHeight=60, distanceBetweenWheels=50, wheelsRadius=8):
        rep = Rectangle(robotWidth, robotHeight, random.choice(self.COLORS), self.DEFAULT_BORDER_RADIUS)
        super().__init__(x, y, orientation, Representation(rep))
        self._leftFrontWheel = Wheel(-distanceBetweenWheels / 2 + 4, -robotHeight/4, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._rightFrontWheel = Wheel(distanceBetweenWheels / 2 - 4, -robotHeight/4, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._leftBackWheel = Wheel(-distanceBetweenWheels / 2 + 4, robotHeight/5, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._rightBackWheel = Wheel(distanceBetweenWheels / 2 - 4,robotHeight/5, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftFrontWheel)
        self.addComponent(self._rightFrontWheel)
        self.addComponent(self._leftBackWheel)
        self.addComponent(self._rightBackWheel)
        self._distanceBetweenWheels = distanceBetweenWheels


    def move(self):

        # vitesse élémentaire (addition des couples donnée par chaque roues motrices)
        rightElementarySpeed = (self._rightFrontWheel.getRadius() * self._rightFrontWheel.getSpeed() * self._rightFrontWheel.getCW()+self._rightBackWheel.getRadius() * self._rightBackWheel.getSpeed() * self._rightBackWheel.getCW()) * config["time_step"] / 60
        leftElementarySpeed = (self._leftFrontWheel.getRadius() * self._leftFrontWheel.getSpeed() * self._leftFrontWheel.getCW()+self._leftBackWheel.getRadius() * self._leftBackWheel.getSpeed() * self._leftBackWheel.getCW()) * config["time_step"] / 60

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

    def setLeftFrontWheelSpeed(self,speed):
        self._leftFrontWheel.setSpeed(speed)

    def setRightFrontWheelSpeed(self,speed):
        self._rightFrontWheel.setSpeed(speed)

    def setLeftBackWheelSpeed(self,speed):
        self._leftBackWheel.setSpeed(speed)

    def setRightBackWheelSpeed(self,speed):
        self._rightBackWheel.setSpeed(speed)

