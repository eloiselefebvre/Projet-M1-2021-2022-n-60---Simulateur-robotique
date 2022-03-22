from abc import abstractmethod
from discoverySimulator import Component
from discoverySimulator.representation.Representation import Representation


class Sensor(Component):
    """
    This method is used to create a new sensor
    """
    def __init__(self,representation:Representation):
       super().__init__(representation)

    @abstractmethod
    def refresh(self):
        pass

