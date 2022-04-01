from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Rectangle import Rectangle


class RectangularObstacle(Obstacle):

    """ The RectangularObstacle class provides a rectangular obstacle and his representation."""

    def __init__(self,width:float,height:float,color:str=None,borderRadius:float=0,opacity:int=255):
        """
        Constructs an obstacle.
        @param width  Width of the obstacle
        @param height  Height of the obstacle
        @param color  Color of the shape
        @param borderRadius  Border of the shape
        @param opacity  Opacity of the shape"""
        rep=Representation(Rectangle(width,height,color,borderRadius,opacity))
        super().__init__(rep)