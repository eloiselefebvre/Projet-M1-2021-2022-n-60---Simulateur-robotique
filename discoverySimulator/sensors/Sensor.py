from abc import abstractmethod
from discoverySimulator import Component

class Sensor(Component):
    """
    This method is used to create a new sensor
    """
    def __init__(self,representation):
       super().__init__(representation)

    @abstractmethod
    def refresh(self):
        pass

