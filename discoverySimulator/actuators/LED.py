from . import Actuator
from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle


class LED(Actuator):

    """ The LED class provides the representation and behavior of an LED.
    The LED can have the desired color and its state can be chosen at will (ON or OFF)."""

    RED = colors["red"]
    GREEN = colors["green"]
    BLUE = colors["blue"]
    YELLOW = colors["yellow"]

    LOW=False
    HIGH=True

    __LOW_OPACITY=56
    __HIGH_OPACITY=255

    def __init__(self,color:str=None):
        """ Constructs a LED.
        @param color  Color of the LED"""
        self._representation = Representation(Circle(5,LED.RED if color is None else color,20))
        super().__init__(self._representation)
        self.__state=False

    # SETTERS
    def setState(self,state:bool):
        """" Sets the state of the LED with a boolean.
        @param state  State of the LED: True to turn ON the LED, False to turn OFF"""
        if state!=self.__state:
            self.__state=state
            if self.__state==LED.HIGH:
                self._representation.getShape().setOpacity(LED.__HIGH_OPACITY)
            else:
                self._representation.getShape().setOpacity(LED.__LOW_OPACITY)
        self.notifyObservers("stateChanged")

    def toggleState(self):
        """ Toggles the state of the LED."""
        self.setState(not self.__state)

    # GETTERS
    def getState(self) -> bool:
        """ Returns the state of the LED."""
        return self.__state

    def getSpecifications(self) -> str:
        return f"Current state : {'ON' if self.__state else 'OFF'}"



