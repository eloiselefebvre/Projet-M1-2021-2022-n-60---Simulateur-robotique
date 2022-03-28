from PyQt5.QtGui import QColor

class Border:

    """ The Border class provides ...."""

    def __init__(self,width:int=0,color:str=None):
        self.__width = int(width)
        self.__color = QColor(color)

    # GETTERS
    def getWidth(self) -> int:
        """
        This method allows to get the width of a border
        :return:
        """
        return self.__width

    def getColor(self) -> str:
        """
        This method allows to get the color of a border
        :return:
        """
        return self.__color