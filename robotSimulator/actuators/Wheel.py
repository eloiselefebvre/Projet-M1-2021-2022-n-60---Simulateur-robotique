from . import Actuator
from robotSimulator.representation.shapes import Rectangle, Border
from robotSimulator.representation import Representation


class Wheel(Actuator):

    DEFAULT_BORDER_RADIUS = 3
    DEFAULT_BORDER_WIDTH = 2

    def __init__(self,x,y,radius,width,orientation=0):
        shape = Rectangle(width,2*radius,"#1C1E32",self.DEFAULT_BORDER_RADIUS)
        shape.addBorder(Border(self.DEFAULT_BORDER_WIDTH,'#f3f3f3'))
        super().__init__(x,y,orientation,Representation(shape))
        self._speed=0
        self._radius = radius

    def setSpeed(self,speed): # En tour/min
        self._speed = speed

    def getSpeed(self):
        return self._speed

    def getRadius(self):
        return self._radius

