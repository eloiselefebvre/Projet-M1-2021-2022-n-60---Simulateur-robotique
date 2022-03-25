from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Rectangle import Rectangle
from discoverySimulator.representation.Representation import Representation
import random

class RectangularTwoWheelsRobot(TwoWheelsRobot):

    def __init__(self, color=None, robotWidth:float=50, robotHeight:float=60, distanceBetweenWheels:float=50, wheelsRadius:float=10, wheelYPosition:float=0):
        """ This method allows to create a rectangle two wheels robot
        @param color  color of the robot
        @param robotWidth  width of the robot [px]
        @param robotHeight  height of the robot [px]
        @param distanceBetweenWheels  distance between wheels [px]
        @param wheelsRadius  radius of wheels [px]
        @param wheelYPosition  position of the two wheels on the robot [px]
        """
        color = random.choice(TwoWheelsRobot.COLORS) if color is None else color
        rep=Rectangle(robotWidth,robotHeight,color,self.DEFAULT_BORDER_RADIUS)
        rep.addOrientationMark()
        super().__init__(Representation(rep), distanceBetweenWheels, wheelsRadius, wheelYPosition)
