from robotSimulator.actuators.Actuator import Actuator
from robotSimulator.representation.shapes.Rectangle import Rectangle
from robotSimulator.representation.Representation import Representation
from robotSimulator.representation.shapes.Border import Border

class Wheel(Actuator):

    def __init__(self,x,y,radius,width,orientation=0):
        shape = Rectangle(width,2*radius,"#1C1E32",3)
        shape.addBorder(Border(2,'#f3f3f3'))
        super().__init__(x,y,orientation,Representation(shape))
        self._speed=0

    def setSpeed(self,speed):
        self._speed = speed

    def getSpeed(self):
        return self._speed

    def getRadius(self):
        return self._radius

