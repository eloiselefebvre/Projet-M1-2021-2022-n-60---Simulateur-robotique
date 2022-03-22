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

    def setSpeed(self,speed):
        """
        This method allows to change the speed of a wheel
        :param speed: new speed of a wheel [rpm]
        """
        self._speed = speed
        self.notifyObservers("stateChanged")

    def getSpeed(self):
        """
        This method is used to get the speed of a wheel
        :return: the speed of the wheel [rpm]
        """
        return self._speed

    def getRadius(self):
        """
        This method allows to get the radius of a wheel
        :return: the radius of a wheel [px]
        """
        return self._radius

    def getSpecifications(self):
        specifications=f"Current speed : {self._speed}rpm<br>---<br>"
        specifications+=f"Radius : {self._radius}px"
        return specifications

