from .shapes import Shape
from .. import Pose


class Representation:

    """ The Representation class provides ...."""

    def __init__(self,shape):
        """
        This method allows to add a representation of an object
        :param shape: shape of the object
        """
        self.__shape=None
        self.setShape(shape)
        self.__subRepresentations=[]
        self.__pose=None
        self.__visible = True

    # SETTERS
    def setPose(self,pose:Pose):
        """
        This method is used to change the position of a representation
        :param pose: new position of the representation
        """
        self.__pose=pose
        self.__shape.setPose(self.__pose)

    def setShape(self,shape:Shape):
        """
        This method is used to set the shape of an object
        :param shape: shape of the object
        """
        if isinstance(shape,Shape):
            self.__shape=shape

    def setVisible(self,visible:bool):
        """
        This method is used to set the visibility of the representation
        :param visible: if the object is visible
        """
        self.__visible = visible

    # GETTERS
    def getShape(self) -> Shape:
        """
        This method allows to get the shape of a representation
        :return: the shape of the representation
        """
        return self.__shape

    def addSubRepresentation(self, representation):
        """
        This method is used to add a sub representation of a representation
        :param representation: the sub representation to add
        """
        if isinstance(representation, Representation):
            self.__subRepresentations.append(representation)

    def toggleVisible(self):
        """
        This method is used to reverse the visibility of a representation
        """
        self.__visible=not self.__visible

    def isVisible(self) -> bool:
        """
        This method is used to know if a representation is visible
        :return: return if the representation is visible
        """
        return self.__visible

    def paint(self,painter):
        if self.__visible:
            self.__shape.paint(painter)
            for rep in self.__subRepresentations:
                painter.save() # save the state of the painter
                rep.paint(painter)
                painter.restore() # restore the state of the painter

    def contains(self,point) -> bool:
        """
        This method is used to know if a representation contains a point
        :param point: point in the environment
        :return: if the point is in the representation
        """
        return self.__shape.contains(point)
