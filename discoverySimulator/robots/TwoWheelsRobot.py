from math import cos,sin,radians,degrees

from discoverySimulator.config import config
from . import Robot
from discoverySimulator.actuators.Wheel import Wheel

class TwoWheelsRobot(Robot):

    """ The TwoWheelsRobot class provides a two wheels robot."""

    _DEFAULT_WHEEL_WIDTH = 8
    _COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]

    def __init__(self, representation, distanceBetweenWheels:float, wheelsRadius:float, wheelYPosition:float):
        """ Create a two wheels robot.
        @param representation  representation of the robot
        @param distanceBetweenWheels: distance between wheels [px]
        @param wheelsRadius  radius of wheels [px]
        @param wheelYPosition  position of wheels on the robot [px]"""
        super().__init__(representation)
        self._leftWheel = Wheel(wheelsRadius, self._DEFAULT_WHEEL_WIDTH)
        self._rightWheel = Wheel(wheelsRadius, self._DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftWheel, (-distanceBetweenWheels + self._DEFAULT_WHEEL_WIDTH) / 2, wheelYPosition)
        self.addComponent(self._rightWheel, (distanceBetweenWheels - self._DEFAULT_WHEEL_WIDTH) / 2, wheelYPosition)
        self._distanceBetweenWheels = distanceBetweenWheels
        self._leftWheel.setID("LeftWheel")
        self._rightWheel.setID("RightWheel")

    # SETTERS
    def setLeftWheelSpeed(self,speed:int):
        """ Sets the speed of the left wheel.
        @param speed  Speed of the wheel [rpm]"""
        if not self._isSpeedLocked:
            self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed:int):
        """ Sets the speed of the right wheel.
        @param speed  Speed of the wheel [rpm]"""
        if not self._isSpeedLocked:
            self._rightWheel.setSpeed(speed)

    # GETTERS
    def getAverageSpeed(self):
        """ Returns the average speed of an object [rpm]."""
        averageSpeedRobot = (self.getRightElementaryLinearSpeed() + self.getLeftElementaryLinearSpeed()) / 2
        return averageSpeedRobot

    def getRightWheel(self) -> Wheel:
        """Returns the speed of the right wheel [rpm]."""
        return self._rightWheel

    def getLeftWheel(self) -> Wheel:
        """ Returns the speed of the left wheel [rpm]."""
        return self._leftWheel

    def getRightLinearSpeed(self) -> float:
        """ Returns the linear speed of the right wheel [px/min]."""
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed()

    def getRightElementaryLinearSpeed(self) -> float:
        """ Returns the elementary speed of the right wheel [px/timestep]."""
        return self.getRightLinearSpeed()*config["real_update_time_step"] / 60

    def getLeftLinearSpeed(self) -> float:
        """ Returns the linear speed of the left wheel [px/min]."""
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed()

    def getLeftElementaryLinearSpeed(self) -> float:
        """ Returns the elementary speed of the left wheel [px/timestep]."""
        return self.getLeftLinearSpeed() * config["real_update_time_step"] / 60

    def getDistanceBetweenWheels(self) -> float:
        """ Returns the distance between wheels [px]."""
        return self._distanceBetweenWheels

    def move(self):
        if not self._isCollided:
            # average speed of the robot
            averageSpeedRobot = (self.getRightElementaryLinearSpeed() + self.getLeftElementaryLinearSpeed()) / 2

            # speed along the x and y axes
            Phi = radians(self._pose.getOrientation() + 90)
            dx = averageSpeedRobot * cos(Phi)
            dy = averageSpeedRobot * sin(Phi)

            # angular speed
            dPhi = -degrees((self.getRightElementaryLinearSpeed() - self.getLeftElementaryLinearSpeed()) / (2 * self._distanceBetweenWheels)) # indirect benchmark so minus sign

            self._pose.move(self._pose.getX() + dx, self._pose.getY() + dy)
            self._pose.rotate(dPhi)

            self.computeCollisions()
        super().move()

    def computeRotationCenter(self):
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX()) / 2,
                                         (self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY()) / 2)



