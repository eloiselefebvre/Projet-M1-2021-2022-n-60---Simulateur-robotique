from discoverySimulator.Object import Object


class Obstacle(Object):

    """ The Obstacle class provides an obsacle and his representation."""

    def __init__(self,representation):
        """ Constructs a new obstacle.
        @param representation  Representation of the obstacle"""
        super().__init__(representation)
