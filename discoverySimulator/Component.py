from abc import ABC, abstractmethod
from discoverySimulator.Object import Object
from discoverySimulator.representation.Representation import Representation


class Component(ABC,Object):

    def __init__(self,representation:Representation):
        """
        This method is used to create a component
        :param representation: representation of the component
        """
        super().__init__(representation)
        self._parent = None

    # SETTERS
    def setParent(self,parent):
        self._parent = parent

    # GETTERS
    @abstractmethod
    def getSpecifications(self): # TODO : Styliser avec HTML
        pass


