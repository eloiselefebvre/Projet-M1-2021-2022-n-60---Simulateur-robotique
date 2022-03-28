from . import Actuator
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle


class LED(Actuator):

    """ The LED class provides ...."""

    RED = "#f00"
    GREEN = "#0f0"
    BLUE = "#00f"
    YELLOW = "#ff0"

    LOW=False
    HIGH=True

    __LOW_OPACITY=40 # TODO : Faire ça partout pour les attributs statiques privés
    __HIGH_OPACITY=255

    def __init__(self,color:str):
        """ This method is used to create a new LED
        @param color  Color of the LED
        """
        self._representation = Representation(Circle(5,color,20))
        super().__init__(self._representation)
        self._state=False
        self._color = color

    # SETTERS
    def setState(self,state:bool):
        """ This method allows to change the state of a LED.
        @param state  State of the LED.
        """
        if state!=self._state:
            self._state=state
            if self._state==LED.HIGH:
                self._representation.getShape().setOpacity(LED.__HIGH_OPACITY)
            else:
                self._representation.getShape().setOpacity(LED.__LOW_OPACITY)
        self.notifyObservers("stateChanged")

    # GETTERS
    def getState(self) -> bool:
        """ This method is used to get the state of a LED.
        @return  The state of the LED.
        """
        return self._state

    def getSpecifications(self) -> str:
        """ This method allows to get specifications about a LED.
        @return  Specifications.
        """
        return f"Current state : {'ON' if self._state else 'OFF'}"



