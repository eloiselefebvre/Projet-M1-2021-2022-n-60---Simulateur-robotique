from abc import abstractmethod
from discoverySimulator import Component


class Sensor(Component):

    """ The Sensor class provides a sensor."""

    def __init__(self,representation):
       """ Constructs a sensor."""
       super().__init__(representation)

    @abstractmethod
    def refresh(self):
        pass

