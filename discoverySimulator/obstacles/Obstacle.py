from discoverySimulator.Object import Object


class Obstacle(Object):

    instances_counter=0

    def __init__(self,representation):
        super().__init__(representation)

