from . import RectangularTwoWheelsRobot
from discoverySimulator.actuators.Wheel import Wheel
from discoverySimulator.config import *

class FourWheelsRobot(RectangularTwoWheelsRobot):

    def __init__(self, color:str=None, robotWidth:int=50, robotHeight:int=60, distanceBetweenWheels:int=50, wheelsRadius:int=10, frontWheelYPosition:int=15, backWheelYPosition:int=-15):
        """ This method is used to create a four wheels robot
        @param color  Color of the robot
        @param robotWidth  Width of the robot [px]
        @param robotHeight  Height of the robot [px]
        @param distanceBetweenWheels  Distances between wheels [px]
        @param wheelsRadius  Radius of wheels [px]
        @param frontWheelYPosition  Position of the two front wheels [px]
        @param backWheelYPosition  Position of the two back wheels [px]
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

    # SETTERS
    def setLeftFrontWheelSpeed(self, speed: int):
        """ This method is used to set the speed of the left front wheel
        @param speed  Speed of the wheel [rpm]
        """
        self.setLeftWheelSpeed(speed)

    def setRightFrontWheelSpeed(self, speed: int):
        """ This method is used to set the speed of the right front wheel
        @param speed  Speed of the wheel [rpm]
        """
        self.setRightWheelSpeed(speed)

    def setLeftBackWheelSpeed(self, speed: int):
        """ This method is used to set the speed of the left back wheel
        @param speed Speed of the wheel [rpm]
        """
        if not self._isSpeedLocked:
            self._backLeftWheel.setSpeed(speed)

    def setRightBackWheelSpeed(self, speed: int):
        """ This method is used to set the speed of the right back wheel
        @param speed  Speed of the wheel [rpm]
        """
        if not self._isSpeedLocked:
            self._backRightWheel.setSpeed(speed)

    def setBackWheelY(self, y: int):
        """ This method allows to change the position of the two back wheels
        @param y  The new position
        """
        self._backRightWheel.getPose().setY(y)
        self._backLeftWheel.getPose().setY(y)

    # GETTERS
    def getRightLinearSpeed(self) -> float:
        """ This method is used to get the right linear speed
        @return  The right linear speed
        """
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed() + self._backRightWheel.getRadius() * self._backRightWheel.getSpeed()

    def getRightElementarySpeed(self) -> float:
        """ This method is used to get the right elementary speed
        @return  The right elementary speed
        """
        return config["real_update_time_step"] / 60 * (
                    self._rightWheel.getRadius() * self._rightWheel.getSpeed() + self._backRightWheel.getRadius() * self._backRightWheel.getSpeed()) * self._acceleration

    def getLeftLinearSpeed(self) -> float:
        """ This method is used to get the elft linear speed
        @return  The left linear speed
        """
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._backLeftWheel.getRadius() * self._backLeftWheel.getSpeed()

    def getLeftElementarySpeed(self) -> float:
        """ This method is used to get the right elementary speed
        @return  The right elementary speed
        """
        return config["real_update_time_step"] / 60 * (
                    self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._backLeftWheel.getRadius() * self._backLeftWheel.getSpeed()) * self._acceleration

    def move(self):
        super().move()

    def computeRotationCenter(self):
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX() + self._backRightWheel.getPose().getX() + self._backLeftWheel.getPose().getX()) / 4,(self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY() + self._backRightWheel.getPose().getY() + self._backLeftWheel.getPose().getY()) / 4)



