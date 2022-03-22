from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Rectangle import Rectangle
from discoverySimulator.representation.Representation import Representation
import random

class RectangleTwoWheelsRobot(TwoWheelsRobot):

    def __init__(self, color=None, robotWidth=50, robotHeight=60, distanceBetweenWheels=50, wheelsRadius=10, wheelYPosition=0):
        """
        This method allows to create a rectangle two wheels robot
        :param color: color of the robot
        :param robotWidth: width of the robot [px]
        :param robotHeight: height of the robot [px]
        :param distanceBetweenWheels: distance between wheels [px]
        :param wheelsRadius: radius of wheels [px]
        :param wheelYPosition: position of the two wheels on the robot [px]
        """
        self._color = random.choice(self.COLORS) if color is None else color
        rep=Rectangle(robotWidth,robotHeight,self._color,self.DEFAULT_BORDER_RADIUS)
        rep.addOrientationMark()
        super().__init__(Representation(rep), color, distanceBetweenWheels, wheelsRadius, wheelYPosition)
