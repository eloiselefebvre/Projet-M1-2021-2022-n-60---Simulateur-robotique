from . import Actuator
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle


class LED(Actuator):
    RED = "#f00"
    GREEN = "#0f0"
    BLUE = "#00f"
    YELLOW = "#ff0"

    LOW=0
    HIGH=1

    def __init__(self,color):
        self._representation = Representation(Circle(5,color,20))
        super().__init__(self._representation)
        self._state=0
        self._color = color

    def setState(self,state):
        if state!=self._state:
            self._state=state
            if self._state==LED.HIGH:
                self._representation.getShape().setOpacity(255)
            else:
                self._representation.getShape().setOpacity(40)
        self.notifyObservers("stateChanged")

    def getState(self):
        return self._state

    def getSpecifications(self):
        return f"Current state : {'ON' if self._state else 'OFF'}"