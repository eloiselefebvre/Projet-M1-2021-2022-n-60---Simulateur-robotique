from abc import abstractmethod
from discoverySimulator.Component import Component


class Sensor(Component):
    """ The Sensor class provides a mold to implement sensors."""

    def __init__(self, representation):
        """ Constructs a sensor with the desired representation."""
        super().__init__(representation)

    @abstractmethod
    def refresh(self):
        pass
