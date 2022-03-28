from math import cos,sin,radians,degrees

from discoverySimulator.config import config
from . import Robot
from discoverySimulator.actuators.Wheel import Wheel

class TwoWheelsRobot(Robot):

    _DEFAULT_WHEEL_WIDTH = 8
    _COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]

    def __init__(self, representation, distanceBetweenWheels:float, wheelsRadius:float, wheelYPosition:float):
        """ This method allows to ...
        @param representation  representation of the robot
        @param distanceBetweenWheels: distance between wheels [px]
        @param wheelsRadius  radius of wheels [px]
        @param wheelYPosition  position of wheels on the robot [px]
        """
        super().__init__(representation)
        self._leftWheel = Wheel(wheelsRadius, self._DEFAULT_WHEEL_WIDTH)
        self._rightWheel = Wheel(wheelsRadius, self._DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftWheel, (-distanceBetweenWheels + self._DEFAULT_WHEEL_WIDTH) / 2, wheelYPosition)
        self.addComponent(self._rightWheel, (distanceBetweenWheels - self._DEFAULT_WHEEL_WIDTH) / 2, wheelYPosition)
        self._distanceBetweenWheels = distanceBetweenWheels
        self._leftWheel.setID("LeftWheel")
        self._rightWheel.setID("RightWheel")

    # SETTERS
    def setLeftWheelSpeed(self,speed):
        """ This method allows to change the speed of the left wheel
        @param speed  New speed of the robot [rpm]
        """
        if not self._isSpeedLocked:
            self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed):
        """ This method allows to change the speed of the right wheel
        @param speed  New speed of the robot [rpm]
        """
        if not self._isSpeedLocked:
            self._rightWheel.setSpeed(speed)

    # GETTERS
    def getAverageSpeed(self):
        """ This method is used to get the average speed of an object
        @return  Average speed of the object [rpm]
        """
        averageSpeedRobot = (self.getRightElementarySpeed() + self.getLeftElementarySpeed()) / 2
        return averageSpeedRobot

    def getRightWheel(self) -> Wheel:
        """This method allows to get the speed of the right wheel
        @return  speed of the robot [rpm]
        """
        return self._rightWheel

    def getLeftWheel(self) -> Wheel:
        """This method allows to get the speed of the left wheel
        @return  speed of the robot [rpm]
        """
        return self._leftWheel

    # TODO : Revoir les noms des fonctions
    def getRightLinearSpeed(self) -> float:
        """This method allows to get the linear speed of the right wheel
        @return  Linear speed of the right wheel
        """
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed()

    def getRightElementarySpeed(self) -> float:
        """ This method allows to get the elementary speed of the right wheel
        @return  elementary speed of the right wheel [rpm]
        """
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed()*config["real_update_time_step"] / 60 * self._acceleration

    def getLeftLinearSpeed(self) -> float:
        """ This method allows to get the linear speed of the left wheel
        @return : linear speed of the left wheel
        """
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed()

    def getLeftElementarySpeed(self) -> float:
        """
        This method allows to get the elementary speed of the left wheel
        @return  elementary speed of the left wheel [rpm]
        """
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed() * config["real_update_time_step"] / 60 * self._acceleration

    def getDistanceBetweenWheels(self) -> float:
        """ This method is used to get the distance between wheels
        @return  distance between wheels [px]
        """
        return self._distanceBetweenWheels

    def move(self):
        if not self._isCollided:
            # average speed of the robot
            averageSpeedRobot = (self.getRightElementarySpeed() + self.getLeftElementarySpeed()) / 2

            # speed along the x and y axes
            Phi = radians(self._pose.getOrientation() + 90)
            dx = averageSpeedRobot * cos(Phi)
            dy = averageSpeedRobot * sin(Phi)

            # angular speed
            dPhi = degrees((self.getRightElementarySpeed() - self.getLeftElementarySpeed())/(2*self._distanceBetweenWheels))

            self._pose.move(self._pose.getX() + dx, self._pose.getY() + dy)
            self._pose.rotate(dPhi)

            self.isCollided()

        super().move()

    def computeRotationCenter(self):
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX()) / 2,
                                         (self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY()) / 2)



