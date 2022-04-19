from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Circle import Circle


class CircularObstacle(Obstacle):

    """ The CircularObstacle class provides a circular obstacle object.
    It is a comfort class avoiding the manipulation of Shape and Representation classes."""

    def __init__(self,radius:float,color:str=None,opacity:int=255):
        """ Constructs a circular obstacle.
        @param radius  Radius of the obstacle
        @param color  Color of the obstacle
        @param opacity  Opacity of the obstacle"""
        rep=Representation(Circle(radius,color,opacity))
        super().__init__(rep)