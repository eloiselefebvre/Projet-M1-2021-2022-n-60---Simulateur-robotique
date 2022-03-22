from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Rectangle import Rectangle


class RectangularObstacle(Obstacle):

    def __init__(self,width,height,color=None,borderRadius=0,opacity=255):
        rep=Representation(Rectangle(width,height,color,borderRadius,opacity))
        super().__init__(rep)