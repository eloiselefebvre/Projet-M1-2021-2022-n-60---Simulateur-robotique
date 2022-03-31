from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Circle import Circle


class CircularObstacle(Obstacle):

    """ The CircularObstacle class provides a circular obstacle and his representation"""

    def __init__(self,radius:float,color:str=None,opacity:int=255):
        """
        Constructs a circular obstacle
        @param radius  the radius of the obstacle
        @param color  the color of the obstacle
        @param opacity  the opacity of the obstacle
        """
        rep=Representation(Circle(radius,color,opacity))
        super().__init__(rep)