from . import TwoWheelsRobot
from discoverySimulator.actuators.Wheel import Wheel

from discoverySimulator.config import *

class FourWheelsRobot(TwoWheelsRobot):
    instances_counter=0

    def __init__(self,color=None,robotWidth=50,robotHeight=60,distanceBetweenWheels=50,wheelsRadius=10,frontWheelYPos=15,backWheelYPos=-15):
        super().__init__(color,robotWidth,robotHeight,distanceBetweenWheels,wheelsRadius,frontWheelYPos)
        self._backLeftWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._backRightWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._backLeftWheel, (distanceBetweenWheels - TwoWheelsRobot.DEFAULT_WHEEL_WIDTH)/2, backWheelYPos)
        self.addComponent(self._backRightWheel, (-distanceBetweenWheels + TwoWheelsRobot.DEFAULT_WHEEL_WIDTH)/2, backWheelYPos)
        self._backLeftWheel.setID("BackLeftWheel")
        self._backRightWheel.setID("BackRightWheel")
        self._leftWheel.setID("FrontLeftWheel")
        self._rightWheel.setID("FrontRightWheel")

    def move(self):
        super().move()

    def setRotationCenter(self):
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX() + self._backRightWheel.getPose().getX() + self._backLeftWheel.getPose().getX()) / 4,
                                     (self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY() + self._backRightWheel.getPose().getY() + self._backLeftWheel.getPose().getY()) / 4)


    def getRightLinearSpeed(self):
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed() + self._backRightWheel.getRadius() * self._backRightWheel.getSpeed()

    def getRightElementarySpeed(self):
        return config["update_time_step"] / 60 * (self._rightWheel.getRadius() * self._rightWheel.getSpeed() + self._backRightWheel.getRadius() * self._backRightWheel.getSpeed()) * self._acceleration

    def getLeftLinearSpeed(self):
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._backLeftWheel.getRadius() * self._backLeftWheel.getSpeed()

    def getLeftElementarySpeed(self):
        return config["update_time_step"] / 60 * (self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._backLeftWheel.getRadius() * self._backLeftWheel.getSpeed()) * self._acceleration

    def setLeftFrontWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed)

    def setRightFrontWheelSpeed(self,speed):
        self._rightWheel.setSpeed(speed)

    def setLeftBackWheelSpeed(self,speed):
        self._backLeftWheel.setSpeed(speed)

    def setRightBackWheelSpeed(self,speed):
        self._backRightWheel.setSpeed(speed)

    def setBackWheelY(self,y):
        self._backRightWheel.getPose().setY(y)
        self._backLeftWheel.getPose().setY(y)

