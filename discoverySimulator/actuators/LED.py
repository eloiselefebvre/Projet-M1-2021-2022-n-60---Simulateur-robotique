from . import Actuator
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle


class LED(Actuator):

    RED = "#f00"
    GREEN = "#0f0"
    BLUE = "#00f"
    YELLOW = "#ff0"

    LOW=False
    HIGH=True

    LOW_OPACITY=40
    HIGH_OPACITY=255

    def __init__(self,color:str):
        """
        This method is used to create a new LED
        :param color: color of the LED
        """
        self._representation = Representation(Circle(5,color,20))
        super().__init__(self._representation)
        self._state=False
        self._color = color

    def setState(self,state:bool):
        """
        This method allows to change the state of a LED
        :param state: state of the LED
        """
        if state!=self._state:
            self._state=state
            if self._state==LED.HIGH:
                self._representation.getShape().setOpacity(LED.HIGH_OPACITY)
            else:
                self._representation.getShape().setOpacity(LED.LOW_OPACITY)
        self.notifyObservers("stateChanged")

    def getState(self) -> bool:
        """
        This method is used to get the state of a LED
        :return: the state of the LED
        """
        return self._state

    def getSpecifications(self) -> str:
        return f"Current state : {'ON' if self._state else 'OFF'}"



