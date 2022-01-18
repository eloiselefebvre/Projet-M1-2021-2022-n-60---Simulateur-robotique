from PyQt5.QtGui import QColor


class Border:

    def __init__(self,width=0,color=None): # et borderRadius ?
        self._width = width
        self._color = QColor(color)

    def getWidth(self):
        return self._width

    def getColor(self):
        return self._color