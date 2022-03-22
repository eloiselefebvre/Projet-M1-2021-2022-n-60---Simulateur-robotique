from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Rectangle import Rectangle
from discoverySimulator.representation.Representation import Representation

import random

class RectangularTwoWheelsRobot(TwoWheelsRobot):

    def __init__(self,color=None,robotWidth=50,robotHeight=60,distanceBetweenWheels=50,wheelsRadius=10,wheelYPos=0):
        self._color = random.choice(self.COLORS) if color is None else color

        rep=Rectangle(robotWidth,robotHeight,self._color,self.DEFAULT_BORDER_RADIUS)
        rep.addOrientationMark()
        super().__init__(Representation(rep),color,distanceBetweenWheels,wheelsRadius,wheelYPos)
