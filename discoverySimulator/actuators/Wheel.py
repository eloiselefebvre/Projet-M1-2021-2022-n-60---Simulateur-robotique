from . import Actuator
from discoverySimulator.representation.shapes import Rectangle, Border
from discoverySimulator.representation import Representation


class Wheel(Actuator):

    DEFAULT_BORDER_RADIUS = 3
    DEFAULT_BORDER_WIDTH = 2

    def __init__(self,radius,width):
        shape = Rectangle(width,2*radius,"#1C1E32",self.DEFAULT_BORDER_RADIUS)
        shape.addBorder(Border(self.DEFAULT_BORDER_WIDTH,'#f3f3f3'))
        super().__init__(Representation(shape))
        self._speed=0
        self._radius = radius

    def setSpeed(self,speed): # En tour/min
        self._speed = speed
        self.notifyObservers("stateChanged")

    def getSpeed(self):
        return self._speed

    def getRadius(self):
        return self._radius

    def getSpecifications(self):
        specifications=f"Current speed : {self._speed}rpm\n---\n"
        specifications+=f"Radius : {self._radius}px"
        return specifications

