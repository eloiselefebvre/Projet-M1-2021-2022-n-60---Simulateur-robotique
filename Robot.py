from Object import Object
from Component import Component

class Robot(Object):
    def __init__(self,xPos,yPos,orientation,representation):
        super().__init__(xPos,yPos,orientation,representation)
        self._components=[]

    def addComponent(self,comp):
        if isinstance(comp,Component):
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    def move(self,dx,dy):
        self._xPos+=dx
        self._yPos+=dy
        self._representation.setParameters(self._xPos, self._yPos,self._orientation)
