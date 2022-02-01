from abc import ABC, abstractmethod

from robotSimulator import Object
from robotSimulator import Component
from robotSimulator import Pose

class Robot(ABC,Object):

    def __init__(self,representation):
        super().__init__(representation)
        self._components=[]

    def addComponent(self,comp,x,y,orientation=0):
        if isinstance(comp,Component):
            comp.setPose(Pose(x,y,orientation))
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    @abstractmethod
    def move(self):
        pass