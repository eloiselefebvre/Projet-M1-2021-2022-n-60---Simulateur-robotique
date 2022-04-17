from PyQt5.QtGui import QColor

class Border:

    """ The Border class provides a border."""

    def __init__(self,width:int=0,color:str=None):
        self.__width = int(width)
        self.__color = QColor(color)

    # GETTERS
    def getWidth(self) -> int:
        """ Returns the width of a border."""
        return self.__width

    def getColor(self) -> str:
        """ Returns the color of a border."""
        return self.__color