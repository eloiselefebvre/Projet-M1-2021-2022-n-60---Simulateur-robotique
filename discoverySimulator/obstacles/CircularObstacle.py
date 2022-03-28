from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Circle import Circle


class CircularObstacle(Obstacle):

    """ The CircularObstacle class provides ...."""

    def __init__(self,radius:float,color:str=None,opacity:int=255):
        rep=Representation(Circle(radius,color,opacity))
        super().__init__(rep)