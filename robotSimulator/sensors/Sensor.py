from robotSimulator.Component import Component

class Sensor(Component):
    def __init__(self,x,y,orientation,representation):
        super().__init__(x,y,orientation,representation)