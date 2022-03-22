from math import cos,sin,radians,degrees
from discoverySimulator.config import config
from . import Robot
from discoverySimulator.actuators.Wheel import Wheel

class TwoWheelsRobot(Robot):

    DEFAULT_WHEEL_WIDTH = 8
    DEFAULT_BORDER_RADIUS = 3
    COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]

    def __init__(self, representation, color, distanceBetweenWheels, wheelsRadius, wheelYPosition):
        """
        This method allows to
        :param representation: representation of the robot
        :param color: color of the robot
        :param distanceBetweenWheels: distance between wheels [px]
        :param wheelsRadius: radius of wheels [px]
        :param wheelYPosition: position of wheels on the robot [px]
        """
        super().__init__(representation)
        self._leftWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._rightWheel = Wheel(wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftWheel,(-distanceBetweenWheels+self.DEFAULT_WHEEL_WIDTH)/2,wheelYPosition)
        self.addComponent(self._rightWheel,(distanceBetweenWheels-self.DEFAULT_WHEEL_WIDTH)/2,wheelYPosition)
        self._distanceBetweenWheels = distanceBetweenWheels
        self._leftWheel.setID("LeftWheel")
        self._rightWheel.setID("RightWheel")


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

            self.computeRotationCenter() # TODO : Not each time
            self._pose.move(self._pose.getX() + dx, self._pose.getY() + dy)
            self._pose.rotate(dPhi)

            self.isCollided()

        super().move()

    def getAverageSpeed(self):
        """
        This method is used to get the average speed of an object
        :return: average speed of the object [rmp]
        """
        averageSpeedRobot = (self.getRightElementarySpeed() + self.getLeftElementarySpeed()) / 2
        return averageSpeedRobot

    def computeRotationCenter(self):
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX()) / 2,
                                         (self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY()) / 2)

    def setLeftWheelSpeed(self,speed):
        """
        This method allows to change the speed of the left wheel
        :param speed: new speed of the robot [rpm]
        """
        self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed):
        """
        This method allows to change the speed of the right wheel
        :param speed: new speed of the robot [rpm]
        """
        self._rightWheel.setSpeed(speed)

    def getRightWheel(self):
        """
        This method allows to get the speed of the right wheel
        :return : speed of the robot [rpm]
        """
        return self._rightWheel

    def getLeftWheel(self):
        """
        This method allows to get the speed of the left wheel
        :return : speed of the robot [rpm]
        """
        return self._leftWheel

    def getRightLinearSpeed(self):
        """
        This method allows to get the linear speed of the right wheel
        :return : linear speed of the right wheel [rpm]
        """
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed()

    def getRightElementarySpeed(self):
        """
        This method allows to get the elementary speed of the right wheel
        :return : elementary speed of the right wheel [rpm]
        """
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed()*config["update_time_step"] / 60 * self._acceleration

    def getLeftLinearSpeed(self):
        """
        This method allows to get the linear speed of the left wheel
        :return : linear speed of the left wheel [rpm]
        """
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed()

    def getLeftElementarySpeed(self):
        """
        This method allows to get the elementary speed of the left wheel
        :return : elementary speed of the left wheel [rpm]
        """
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed() * config["update_time_step"] / 60 * self._acceleration

    def setWheelY(self,y):
        """
        This method allows to change the position of wheels on the robot
        :param y: y coordinate of wheels on the robot
        """
        self._rightWheel.getRepresentation().getOrigin().setY(y)
        self._leftWheel.getRepresentation().getOrigin().setY(y)

    def getDistanceBetweenWheels(self):
        """
        This method is used to get the distance between wheels
        :return: distance between wheels [px]
        """
        return self._distanceBetweenWheels

