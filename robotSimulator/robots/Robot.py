from abc import ABC, abstractmethod

from robotSimulator import Object
from robotSimulator import Component

class Robot(ABC,Object):
    def __init__(self,x,y,orientation,representation):
        super().__init__(x,y,orientation,representation)
        self._components=[]

    def addComponent(self,comp):
        if isinstance(comp,Component):
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    @abstractmethod
    def move(self):
        pass