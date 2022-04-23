from discoverySimulator.Component import Component
from discoverySimulator.representation.Representation import Representation


class Actuator(Component):

    """ The Actuator class provides a mold to implement actuators.
    The simulator already offers some actuators that can be completed as needed."""

    def __init__(self,representation:Representation):
        """ Constructs an actuator.
        @param representation  Representation of the actuator"""
        super().__init__(representation)

