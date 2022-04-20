from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Rectangle import Rectangle
from discoverySimulator.representation.Representation import Representation
import random

class RectangularTwoWheelsRobot(TwoWheelsRobot):

    """ The RectangleTwoWheelsRobot class provides a rectangular two wheels robot.
    It is a comfort class avoiding the manipulation of Shape and Representation classes."""

    __DEFAULT_BORDER_RADIUS = 3

    def __init__(self, color:str=None, width:float=50, height:float=60, distanceBetweenWheels:float=48, wheelsRadius:float=10, wheelYPosition:float=0):
        """ Constructs a two wheels robot with a rectangular shape.
        @param color  Color of the robot [hex]
        @param width  Width of the robot [px]
        @param height  Height of the robot [px]
        @param distanceBetweenWheels  Distance between the wheels of the robot [px]
        @param wheelsRadius  Radius of wheels [px]
        @param wheelYPosition  y-position of the wheels on the robot [px]"""
        color = random.choice(TwoWheelsRobot._COLORS) if color is None else color
        rep=Rectangle(width, height, color, RectangularTwoWheelsRobot.__DEFAULT_BORDER_RADIUS)
        rep.addOrientationMark()
        super().__init__(Representation(rep), distanceBetweenWheels, wheelsRadius, wheelYPosition)
