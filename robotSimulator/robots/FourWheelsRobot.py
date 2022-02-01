from . import TwoWheelsRobot
from robotSimulator.representation.shapes import Rectangle
from robotSimulator.representation import Representation
from robotSimulator.actuators import Wheel
import random
from math import cos,sin,radians,degrees

from robotSimulator.config import *

class FourWheelsRobot(TwoWheelsRobot):

    DEFAULT_WHEEL_WIDTH = 8
    DEFAULT_BORDER_RADIUS = 3

    def __init__(self,color=None,robotWidth=50,robotHeight=60,distanceBetweenWheels=50,wheelsRadius=10):
        super().__init__(color,robotWidth=50,robotHeight=60,distanceBetweenWheels=50,wheelsRadius=10)
        self._leftBackWheel = Wheel( wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._rightBackWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftBackWheel,-distanceBetweenWheels / 2 + 4, -robotHeight/5)
        self.addComponent(self._rightBackWheel,distanceBetweenWheels / 2 - 4,-robotHeight/5)
        self.setFrontWheelY(robotHeight/5)

    def move(self):
        super().move()

    def getRightElementarySpeed(self):
        return config["time_step"] / 60 * (self._rightWheel.getRadius() * self._rightWheel.getSpeed() +self._rightBackWheel.getRadius() * self._rightBackWheel.getSpeed())

    def getLeftElementarySpeed(self):
        return config["time_step"] / 60 * (self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._leftBackWheel.getRadius() * self._leftBackWheel.getSpeed())

    def setLeftFrontWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed)

    def setRightFrontWheelSpeed(self,speed):
        self._rightWheel.setSpeed(speed)

    def setLeftBackWheelSpeed(self,speed):
        self._leftBackWheel.setSpeed(speed)

    def setRightBackWheelSpeed(self,speed):
        self._rightBackWheel.setSpeed(speed)

    def setFrontWheelY(self,y):
        self._rightWheel.getRepresentation().getOrigin().setY(y)
        self._leftWheel.getRepresentation().getOrigin().setY(y)

    def setBackWheelY(self,y):
        self._rightBackWheel.getRepresentation().getOrigin().setY(y)
        self._leftBackWheel.getRepresentation().getOrigin().setY(y)