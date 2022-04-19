from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Rectangle import Rectangle


class RectangularObstacle(Obstacle):

    """ The RectangularObstacle class provides a rectangular obstacle.
    It is a comfort class avoiding the manipulation of Shape and Representation classes."""

    def __init__(self,width:float,height:float,color:str=None,borderRadius:float=0,opacity:int=255):
        """ Constructs a rectangular obstacle.
        @param width  Width of the obstacle
        @param height  Height of the obstacle
        @param color  Color of the shape
        @param borderRadius  Border radius of the shape
        @param opacity  Opacity of the shape"""
        rep=Representation(Rectangle(width,height,color,borderRadius,opacity))
        super().__init__(rep)