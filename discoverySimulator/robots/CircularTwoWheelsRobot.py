from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Circle import Circle
from discoverySimulator.representation.Representation import Representation
import random

class CircularTwoWheelsRobot(TwoWheelsRobot):

    def __init__(self,color=None,robotRadius=28,distanceBetweenWheels=50,wheelsRadius=10,wheelYPos=0):
        self._color = random.choice(self.COLORS) if color is None else color

        rep=Circle(robotRadius,self._color)
        rep.addOrientationMark()
        super().__init__(Representation(rep),color,distanceBetweenWheels,wheelsRadius,wheelYPos)
