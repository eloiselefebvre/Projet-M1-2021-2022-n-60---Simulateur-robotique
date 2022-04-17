from .shapes import Shape
from .. import Pose


class Representation:

    """ The Representation class provides the representation of an object."""

    def __init__(self,shape=None):
        """ Adds a representation of an object.
        @param shape  shape of the object"""
        self.__shape=shape
        self.setShape(self.__shape)
        self.__subRepresentations=[]
        self.__pose=None
        self.__visible = True

    # SETTERS
    def setPose(self,pose:Pose):
        self.__pose=pose
        self.__shape.setPose(self.__pose)

    def setShape(self,shape:Shape):
        if isinstance(shape,Shape):
            self.__shape=shape

    def setVisible(self,visible:bool):
        self.__visible = visible

    # GETTERS
    def getShape(self) -> Shape:
        """ Returns the shape of a representation."""
        return self.__shape

    def addSubRepresentation(self, representation):
        """ Adds a sub representation of a representation.
        @param representation  the sub representation to add"""
        if isinstance(representation, Representation):
            self.__subRepresentations.append(representation)

    def toggleVisible(self):
        self.__visible=not self.__visible

    def isVisible(self) -> bool:
        return self.__visible

    def paint(self,painter):
        if self.__visible:
            self.__shape.paint(painter)
            for rep in self.__subRepresentations:
                painter.save() # Save the state of the painter
                rep.paint(painter)
                painter.restore() # Restore the state of the painter

    def contains(self,point) -> bool:
        return self.__shape.contains(point)
