from . import Actuator
from discoverySimulator.representation.shapes import Rectangle, Border
from discoverySimulator.representation import Representation

class Wheel(Actuator):

    DEFAULT_BORDER_RADIUS = 3
    DEFAULT_BORDER_WIDTH = 2

    def __init__(self,radius:float,width:float):
        """
        This method is used to create a new wheel
        :param radius: the radius of the wheel [px]
        :param width: the width of the wheel [px]
        """
        shape = Rectangle(width,2*radius,"#1C1E32",Wheel.DEFAULT_BORDER_RADIUS)
        shape.addBorder(Border(Wheel.DEFAULT_BORDER_WIDTH,'#f0f0f0'))
        super().__init__(Representation(shape))
        self._speed=0
        self._radius = int(radius)

    # SETTERS
    def setSpeed(self,speed:int):
        """
        This method allows to change the speed of a wheel
        :param speed: new speed of a wheel [rpm]
        """
        self._speed = int(speed)
        self.notifyObservers("stateChanged")

    # GETTERS
    def getSpeed(self) -> int:
        """
        This method is used to get the speed of a wheel
        :return: the speed of the wheel [rpm]
        """
        return self._speed

    def getRadius(self) -> int:
        """
        This method allows to get the radius of a wheel
        :return: the radius of a wheel [px]
        """
        return self._radius

    def getSpecifications(self) -> str:
        """
        This method allows to get specifications about a wheel
        :return: specifications
        """
        specifications=f"Current speed : {self._speed}rpm<br>---<br>"
        specifications+=f"Radius : {self._radius}px"
        return specifications

