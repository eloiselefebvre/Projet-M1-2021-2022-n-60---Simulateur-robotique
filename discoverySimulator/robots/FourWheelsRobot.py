from . import RectangularTwoWheelsRobot
from discoverySimulator.actuators.Wheel import Wheel

from discoverySimulator.config import *

class FourWheelsRobot(RectangularTwoWheelsRobot):

    def __init__(self, color:str=None, robotWidth:int=50, robotHeight:int=60, distanceBetweenWheels:int=50, wheelsRadius:int=10, frontWheelYPosition:int=15, backWheelYPosition:int=-15):
        """
        This method is used to create a four wheels robot
        :param color: color of the robot
        :param robotWidth: width of the robot [px]
        :param robotHeight: height of the robot [px]
        :param distanceBetweenWheels: distances between wheels [px]
        :param wheelsRadius: radius of wheels [px]
        :param frontWheelYPosition: position of the two front wheels [px]
        :param backWheelYPosition: position of the two back wheels [px]
        """
        super().__init__(color, robotWidth, robotHeight, distanceBetweenWheels, wheelsRadius, frontWheelYPosition)
        self._backLeftWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._backRightWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._backLeftWheel, (-distanceBetweenWheels + RectangularTwoWheelsRobot.DEFAULT_WHEEL_WIDTH) / 2, backWheelYPosition)
        self.addComponent(self._backRightWheel, (distanceBetweenWheels - RectangularTwoWheelsRobot.DEFAULT_WHEEL_WIDTH) / 2, backWheelYPosition)

        self._backLeftWheel.setID("BackLeftWheel")
        self._backRightWheel.setID("BackRightWheel")
        self._leftWheel.setID("FrontLeftWheel")
        self._rightWheel.setID("FrontRightWheel")

    def move(self):
        super().move()

    def computeRotationCenter(self):
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX() + self._backRightWheel.getPose().getX() + self._backLeftWheel.getPose().getX()) / 4,
                                         (self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY() + self._backRightWheel.getPose().getY() + self._backLeftWheel.getPose().getY()) / 4)

    def getRightLinearSpeed(self) -> float:
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed() + self._backRightWheel.getRadius() * self._backRightWheel.getSpeed()

    def getRightElementarySpeed(self) -> float:
        return config["update_time_step"] / 60 * (self._rightWheel.getRadius() * self._rightWheel.getSpeed() + self._backRightWheel.getRadius() * self._backRightWheel.getSpeed()) * self._acceleration

    def getLeftLinearSpeed(self) -> float:
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._backLeftWheel.getRadius() * self._backLeftWheel.getSpeed()

    def getLeftElementarySpeed(self) -> float:
        return config["update_time_step"] / 60 * (self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._backLeftWheel.getRadius() * self._backLeftWheel.getSpeed()) * self._acceleration

    def setLeftFrontWheelSpeed(self,speed:int):
        """
        This method is used to set the speed of the left front wheel
        :param speed: speed of the wheel [rpm]
        """
        if not self._isFollowingPath:
            self._leftWheel.setSpeed(speed)

    def setRightFrontWheelSpeed(self,speed:int):
        """
        This method is used to set the speed of the right front wheel
        :param speed: speed of the wheel [rpm]
        """
        if not self._isFollowingPath:
            self._rightWheel.setSpeed(speed)

    def setLeftBackWheelSpeed(self,speed:int):
        """
        This method is used to set the speed of the left back wheel
        :param speed: speed of the wheel [rpm]
        """
        if not self._isFollowingPath:
            self._backLeftWheel.setSpeed(speed)

    def setRightBackWheelSpeed(self,speed:int):
        """
        This method is used to set the speed of the right back wheel
        :param speed: speed of the wheel [rpm]
        """
        if not self._isFollowingPath:
            self._backRightWheel.setSpeed(speed)

    def setBackWheelY(self,y:int):
        self._backRightWheel.getPose().setY(y)
        self._backLeftWheel.getPose().setY(y)

