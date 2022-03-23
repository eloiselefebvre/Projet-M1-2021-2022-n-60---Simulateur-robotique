from discoverySimulator.Object import Object


class Obstacle(Object):

    def __init__(self,representation):
        """
        This method is used to create a new obstacle
        :param representation: representation of the obstacle
        """
        super().__init__(representation)
