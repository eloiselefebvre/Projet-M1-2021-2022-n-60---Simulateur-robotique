from robotSimulator.components.Component import Component

class Actuator(Component):

    def __init__(self,xPos,yPos,orientation,representation):
        super().__init__(xPos,yPos,orientation,representation)
