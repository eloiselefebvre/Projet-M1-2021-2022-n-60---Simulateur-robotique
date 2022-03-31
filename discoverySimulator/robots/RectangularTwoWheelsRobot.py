from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Rectangle import Rectangle
from discoverySimulator.representation.Representation import Representation
import random

class RectangularTwoWheelsRobot(TwoWheelsRobot):

    """ The RectangleTwhoWheelsRobot class provides a rectangular two wheels robot."""

    __DEFAULT_BORDER_RADIUS = 3

    def __init__(self, color=None, robotWidth:float=50, robotHeight:float=60, distanceBetweenWheels:float=50, wheelsRadius:float=10, wheelYPosition:float=0):
        """ Constructs a rectangular two wheels robot.
        @param color  color of the robot
        @param robotWidth  width of the robot [px]
        @param robotHeight  height of the robot [px]
        @param distanceBetweenWheels  distance between wheels [px]
        @param wheelsRadius  radius of wheels [px]
        @param wheelYPosition  position of the two wheels on the robot [px]
        """
        color = random.choice(TwoWheelsRobot._COLORS) if color is None else color
        rep=Rectangle(robotWidth, robotHeight, color, RectangularTwoWheelsRobot.__DEFAULT_BORDER_RADIUS)
        rep.addOrientationMark()
        super().__init__(Representation(rep), distanceBetweenWheels, wheelsRadius, wheelYPosition)
