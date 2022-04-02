from . import Actuator
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle


class LED(Actuator):

    """ The LED class provides a LED and his representation."""

    RED = "#f00"
    GREEN = "#0f0"
    BLUE = "#00f"
    YELLOW = "#ff0"

    LOW=False
    HIGH=True

    __LOW_OPACITY=40
    __HIGH_OPACITY=255

    def __init__(self,color:str=None):
        """ Constructs a new LED.
        @param color  Color of the LED"""
        self._representation = Representation(Circle(5,LED.RED if color is None else color,20))
        super().__init__(self._representation)
        self.__state=False

    # SETTERS
    def setState(self,state:bool):
        """" Sets the state of a LED.
        @param state  New state of the LED"""
        if state!=self.__state:
            self.__state=state
            if self.__state==LED.HIGH:
                self._representation.getShape().setOpacity(LED.__HIGH_OPACITY)
            else:
                self._representation.getShape().setOpacity(LED.__LOW_OPACITY)
        self.notifyObservers("stateChanged")

    def toggleState(self):
        self.setState(not self.__state)

    # GETTERS
    def getState(self) -> bool:
        """ Returns the state of a LED."""
        return self.__state

    def getSpecifications(self) -> str:
        return f"Current state : {'ON' if self.__state else 'OFF'}"



