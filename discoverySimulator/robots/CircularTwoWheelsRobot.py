from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Circle import Circle
from discoverySimulator.representation.Representation import Representation
import random

class CircularTwoWheelsRobot(TwoWheelsRobot):

    def __init__(self, color=None, robotRadius=28, distanceBetweenWheels=50, wheelsRadius=10, wheelYPosition=0):
        """
        This method allows to create a circle two wheels robot
        :param color: color of the robot
        :param robotRadius: radius of the robot [px]
        :param distanceBetweenWheels: distance between wheels of the robot [px]
        :param wheelsRadius: radius of the wheels [px]
        :param wheelYPosition: position of the wheels [px]
        """
        self._color = random.choice(self.COLORS) if color is None else color
        rep=Circle(robotRadius,self._color)
        rep.addOrientationMark()
        super().__init__(Representation(rep), color, distanceBetweenWheels, wheelsRadius, wheelYPosition)
