from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Rectangle import Rectangle


class RectangularObstacle(Obstacle):

    def __init__(self,width,height,color=None,borderRadius=0,opacity=255):
        """
        This method is used to create an obstacle
        :param width: width of the obstacle
        :param height: height of the obstacle
        :param color: color of the shape
        :param borderRadius: border of the shape
        :param opacity: opacity of the shape
        """
        rep=Representation(Rectangle(width,height,color,borderRadius,opacity))
        super().__init__(rep)