from abc import ABC, abstractmethod
from discoverySimulator.Object import Object

class Component(ABC,Object):

    def __init__(self,representation):
        """
        This method is used to create a component
        :param representation: representation of the component
        """
        super().__init__(representation)
        self._parent = None

    def setParent(self,parent):
        self._parent = parent

    @abstractmethod
    def getSpecifications(self): # TODO : Styliser avec HTML
        pass


