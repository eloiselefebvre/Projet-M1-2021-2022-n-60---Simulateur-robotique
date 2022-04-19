from PyQt5.QtGui import QColor

class Border:

    """ The Border class provides a border that can be added to a shape."""

    def __init__(self,width:int=0,color:str=None):
        """
        Constructs a border of the desired width and color that can be added to a shape.
        @param width Width of the border
        @param color  Color of the border
        """
        self.__width = int(width)
        self.__color = QColor(color)

    # GETTERS
    def getWidth(self) -> int:
        """ Returns the width of the border."""
        return self.__width

    def getColor(self) -> str:
        """ Returns the color of the border."""
        return self.__color