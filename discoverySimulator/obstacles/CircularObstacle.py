from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Circle import Circle


class CircularObstacle(Obstacle):
    """
    This method is used to create a circular obstacle
    """
    def __init__(self,radius,color,opacity=255):
        rep=Representation(Circle(radius,color,opacity))
        super().__init__(rep)