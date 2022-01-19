from robotSimulator.Object import Object
from robotSimulator.Component import Component

class Robot(Object):
    def __init__(self,x,y,orientation,representation):
        super().__init__(x,y,orientation,representation)
        self._components=[]

    def addComponent(self,comp):
        if isinstance(comp,Component):
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    def move(self):
        pass
        #self._pos.move(self._pos.getX()+dx,self._pos.getY()+dy)
        #self._representation.setParameters(self._pos,self._orientation)
