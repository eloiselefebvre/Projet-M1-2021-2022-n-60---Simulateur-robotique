from PyQt5.QtGui import QColor

class Border:

    def __init__(self,width:int=0,color:str=None):
        self._width = int(width)
        self._color = QColor(color)

    # GETTERS
    def getWidth(self) -> int:
        return self._width

    def getColor(self) -> str:
        return self._color