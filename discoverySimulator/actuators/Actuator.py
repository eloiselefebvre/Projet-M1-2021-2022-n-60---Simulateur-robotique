from discoverySimulator import Component
from discoverySimulator.representation.Representation import Representation


class Actuator(Component):

    """ The Actuator class provides an actuator and his representation."""

    def __init__(self,representation:Representation):
        """ Constructs a new actuator.
        @param representation  Representation of the actuator"""
        super().__init__(representation)

