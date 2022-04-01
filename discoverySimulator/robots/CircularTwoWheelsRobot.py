from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Circle import Circle
from discoverySimulator.representation.Representation import Representation
import random

class CircularTwoWheelsRobot(TwoWheelsRobot):

    """ The CircularTwoWheelsRobot class provides a circular two wheels robot."""

    def __init__(self, color:str=None, robotRadius:int=28, distanceBetweenWheels:int=50, wheelsRadius:int=10, wheelYPosition:int=0):
        """ Constructs a circle two wheels robot.
        @param color  color of the robot
        @param robotRadius  radius of the robot [px]
        @param distanceBetweenWheels  distance between wheels of the robot [px]
        @param wheelsRadius  radius of the wheels [px]
        @param wheelYPosition  position of the wheels [px]"""
        color = random.choice(TwoWheelsRobot._COLORS) if color is None else color
        rep=Circle(robotRadius,color)
        rep.addOrientationMark()
        super().__init__(Representation(rep), distanceBetweenWheels, wheelsRadius, wheelYPosition)
