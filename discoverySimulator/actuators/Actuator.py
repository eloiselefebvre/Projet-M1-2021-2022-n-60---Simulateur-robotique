from discoverySimulator import Component
from discoverySimulator.representation.Representation import Representation


class Actuator(Component):

    """ The Actuator class provides ...."""

    def __init__(self,representation:Representation):
        """ This method is used to create a new actuator
        @param representation  Representation of the actuator
        """
        super().__init__(representation)

