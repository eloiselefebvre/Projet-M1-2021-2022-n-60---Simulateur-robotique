from Robot import Robot
from Rectangle import Rectangle
from Representation import Representation
from Wheel import Wheel

class TwoWheelsRobot(Robot):

    def __init__(self,xPos,yPos,orientation,width=100,radius=50):
        super().__init__(self,xPos,yPos,orientation,Representation(Rectangle(width,2*radius,"#1C1E32",3,2,"#f3f3f3")))
        self._width = 100
        self._radius = 50

    def placeWheels(self):
        wheel = Wheel(0, 10, 10, 8)
        wheel2 = Wheel(42, 10, 10, 8)
