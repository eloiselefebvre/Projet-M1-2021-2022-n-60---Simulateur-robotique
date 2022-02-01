from abc import ABC, abstractmethod
import random

from robotSimulator import Object
from robotSimulator import Component
from robotSimulator.representation.shapes import Point

class Robot(ABC,Object):

    COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]


    def __init__(self,representation,color=None):
        super().__init__(representation)
        self._color = random.choice(self.COLORS) if color is None else color
        self._components=[]

    def addComponent(self,comp,x,y,orientation=0):
        if isinstance(comp,Component):
            comp.setParameters(Point(x,y),orientation)
            self._components.append(comp)
            self._representation.addSubRepresentation(comp.getRepresentation())

    @abstractmethod
    def move(self):
        pass