from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Rectangle import Rectangle
from discoverySimulator.representation.Representation import Representation
import random

class RectangularTwoWheelsRobot(TwoWheelsRobot):

    """ The RectangleTwoWheelsRobot class provides a rectangular two wheels robot."""

    __DEFAULT_BORDER_RADIUS = 3

    def __init__(self, color:str=None, robotWidth:float=50, robotHeight:float=60, distanceBetweenWheels:float=48, wheelsRadius:float=10, wheelYPosition:float=0):
        """ Constructs a rectangular two wheels robot.
        @param color  Color of the robot
        @param robotWidth  Width of the robot [px]
        @param robotHeight  Height of the robot [px]
        @param distanceBetweenWheels  Distance between wheels [px]
        @param wheelsRadius  Radius of wheels [px]
        @param wheelYPosition  Position of the two wheels on the robot [px]"""
        color = random.choice(TwoWheelsRobot._COLORS) if color is None else color
        rep=Rectangle(robotWidth, robotHeight, color, RectangularTwoWheelsRobot.__DEFAULT_BORDER_RADIUS)
        rep.addOrientationMark()
        super().__init__(Representation(rep), distanceBetweenWheels, wheelsRadius, wheelYPosition)
