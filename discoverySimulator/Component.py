from abc import ABC, abstractmethod
from discoverySimulator.Object import Object
from discoverySimulator.representation.Representation import Representation


class Component(ABC,Object):

    """ The Component class provides ...."""

    def __init__(self,representation):
        """ This method is used to create a component.
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
        """ This method allows to get specifications about a wheel.
        @return  Specifications
        """
        pass


