from abc import ABC, abstractmethod
from discoverySimulator.Object import Object
from discoverySimulator.representation.Representation import Representation

class Component(ABC,Object):

    """ The Component class provides a component"""

    def __init__(self,representation):
        """ Constructs a component.
        @param representation  Representation of the component.
        """
        super().__init__(representation)
        self._parent = None

    # SETTERS
    def setParent(self,parent):
        self._parent = parent

    # GETTERS
    @abstractmethod
    def getSpecifications(self):
        """ Returns specifications about a wheel.
        @return  Specifications
        """
        pass


