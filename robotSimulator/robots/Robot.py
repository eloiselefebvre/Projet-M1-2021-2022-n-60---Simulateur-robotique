from abc import ABC, abstractmethod
import random

from robotSimulator import Object
from robotSimulator import Component

class Robot(ABC,Object):

    COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]


    def __init__(self,x,y,orientation,representation,color=None):
        super().__init__(x,y,orientation,representation)
        self._color = random.choice(self.COLORS) if color is None else color
        self._components=[]

    def addComponent(self,comp):
        if isinstance(comp,Component):
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    @abstractmethod
    def move(self):
        pass