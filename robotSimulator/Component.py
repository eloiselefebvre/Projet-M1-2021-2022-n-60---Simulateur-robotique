from abc import ABC, abstractmethod

from robotSimulator.Object import Object

class Component(ABC,Object):
    def __init__(self,representation):
        super().__init__(representation)
        self._parent = None

    def setParent(self,parent):
        self._parent = parent

    @abstractmethod
    def getSpecifications(self):
        pass


