from discoverySimulator.representation.Representation import Representation
from discoverySimulator.Object import Object


class Obstacle(Object):

    """ The Obstacle class provides an obstacle object that can have the chosen shape."""

    def __init__(self,representation:Representation):
        """ Constructs an obstacle with the desired representation.
        @param representation  Representation of the obstacle"""
        super().__init__(representation)
