from . import Actuator
from discoverySimulator.config import colors
from discoverySimulator.representation.shapes import Rectangle, Border
from discoverySimulator.representation import Representation

class Wheel(Actuator):

    """ The Wheel class provides the representation and the behavior of a wheel.
    The speed of the wheel can be changed to control the movement of the robot on which it is mounted."""

    DEFAULT_BORDER_RADIUS = 3
    DEFAULT_BORDER_WIDTH = 2

    def __init__(self,radius:float,width:float):
        """ Constructs a wheel with its radius and thickness.
        @param radius  Radius of the wheel [px]
        @param width  Width of the wheel [px]"""
        shape = Rectangle(width,2*radius,colors["mirage"],Wheel.DEFAULT_BORDER_RADIUS)
        shape.addBorder(Border(Wheel.DEFAULT_BORDER_WIDTH,colors["gallery"]))
        super().__init__(Representation(shape))
        self._speed=0
        self._radius = int(radius)

    # SETTERS
    def setSpeed(self,speed:int):
        """ Sets the speed of the wheel.
        @param speed  Speed of the wheel [rpm]"""
        self._speed = int(speed)
        self.notifyObservers("stateChanged")

    # GETTERS
    def getSpeed(self) -> int:
        """ Returns the speed of the wheel [rpm]."""
        return self._speed

    def getRadius(self) -> int:
        """ Returns the radius of the wheel [px]."""
        return self._radius

    def getSpecifications(self) -> str:
        specifications=f"Current speed : {self._speed}rpm<br><pre>"
        specifications+=f"Radius : {self._radius}px</pre>"
        return specifications

