from Component import Component

class Sensor(Component):
    def __init__(self,xPos,yPos,orientation,representation):
        super().__init__(xPos,yPos,orientation,representation)