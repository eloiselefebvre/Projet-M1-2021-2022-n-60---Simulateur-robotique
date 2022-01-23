from . import Robot
from robotSimulator.representation.shapes import Rectangle
from robotSimulator.representation import Representation
from robotSimulator.actuators import Wheel
import random

class FourWheelsRobot(Robot):

    DEFAULT_WHEEL_WIDTH = 6
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

    def setLeftFrontWheelSpeed(self,speed):
        self._leftWheelSpeed = speed

    def setRightFrontWheelSpeed(self,speed):
        self._rightWheelSpeed = speed

    def setLeftBackWheelSpeed(self,speed):
        self._leftWheelSpeed = speed

    def setRightBackWheelSpeed(self,speed):
        self._rightWheelSpeed = speed


