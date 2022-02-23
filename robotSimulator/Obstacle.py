from robotSimulator.Object import Object


class Obstacle(Object):

    instances_counter=0

    def __init__(self,representation):
        super().__init__(representation)
        Obstacle.instances_counter += 1
        self.completeID(Obstacle.instances_counter)
