from abc import ABC, abstractmethod
from discoverySimulator.Object import Object

class Component(ABC,Object):

    """ The Component class provides a mold to implement components."""

    def __init__(self,representation):
        """ Constructs a component.
        @param representation  Representation of the component."""
        super().__init__(representation)
        self._parent = None

    # SETTERS
    def setParent(self,parent):
        self._parent = parent

    # GETTERS
    @abstractmethod
    def getSpecifications(self):
        pass


