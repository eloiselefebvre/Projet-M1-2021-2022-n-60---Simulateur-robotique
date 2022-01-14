from robotSimulator.components.actuators.Actuator import Actuator
from Rectangle import Rectangle
from Representation import Representation


class Wheel(Actuator):

    def __init__(self,xPos,yPos,radius,width,orientation=0):
        super().__init__(xPos,yPos,orientation,Representation(Rectangle(width,2*radius,"#1C1E32",3,2,"#f3f3f3")))
        self._speed=0

    def setSpeed(self,speed):
        self._speed = speed



