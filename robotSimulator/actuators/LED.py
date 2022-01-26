from . import Actuator
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Circle


class LED(Actuator):
    RED = "#f00"
    GREEN = "#0f0"
    BLUE = "#00f"
    YELLOW = "#ff0"

    LOW=0
    HIGH=1

    def __init__(self,x,y,color):
        self._representation = Representation(Circle(5,color,20))
        super().__init__(x,y,0,self._representation)
        self._state=0
        self._color = color

    def setState(self,state):
        if state!=self._state:
            self._state=state
            if self._state==LED.HIGH:
                self._representation.getRepresentation().setOpacity(255)
            else:
                self._representation.getRepresentation().setOpacity(40)

    def getState(self):
        return self._state