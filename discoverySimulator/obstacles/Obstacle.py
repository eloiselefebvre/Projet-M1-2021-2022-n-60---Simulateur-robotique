from discoverySimulator.Object import Object


class Obstacle(Object):

    instances_counter=0

    def __init__(self,representation):
        """
        This method is used to create a new obstacle
        :param representation: representation of the obstacle
        """
        super().__init__(representation)
