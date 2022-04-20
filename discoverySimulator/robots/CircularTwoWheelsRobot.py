from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Circle import Circle
from discoverySimulator.representation.Representation import Representation
import random

class CircularTwoWheelsRobot(TwoWheelsRobot):

    """ The CircularTwoWheelsRobot class provides a circular two wheels robot.
    It is a comfort class avoiding the manipulation of Shape and Representation classes."""

    def __init__(self, color:str=None, robotRadius:int=28, distanceBetweenWheels:int=50, wheelsRadius:int=10, wheelYPosition:int=0):
        """ Constructs a two wheels robot with a circular shape.
        @param color  Color of the robot [hex]
        @param robotRadius  Radius of the robot [px]
        @param distanceBetweenWheels  Distance between the wheels of the robot [px]
        @param wheelsRadius  Radius of the wheels [px]
        @param wheelYPosition  y-position of the wheels on the robot [px]"""
        color = random.choice(TwoWheelsRobot._COLORS) if color is None else color
        rep=Circle(robotRadius,color)
        rep.addOrientationMark()
        super().__init__(Representation(rep), distanceBetweenWheels, wheelsRadius, wheelYPosition)
