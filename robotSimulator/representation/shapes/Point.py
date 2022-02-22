from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

from robotSimulator.representation.shapes import Shape

class Point(Shape):

    POINT_SIZE = 2

    def __init__(self,x,y,color="#000",opacity=255):
        super().__init__(color,opacity)
        self._x = x
        self._y = y

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def setX(self,x):
        self._x = x

    def setY(self,y):
        self._y = y
        
    def move(self,x,y):
        self._x=x
        self._y=y

    def getLineDecomposition(self):
        return []

    def paint(self,painter):
        super().paint(painter)
        painter.setPen(QPen(self._color, self.POINT_SIZE, Qt.SolidLine))