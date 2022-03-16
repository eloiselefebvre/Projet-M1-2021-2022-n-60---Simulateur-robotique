from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

from discoverySimulator.representation.shapes import Shape
from math import radians, cos, sin

class Point(Shape): # TODO : Hérite de QPoint ? X,Y définisent la pose et translate de X,Y puis drawPoint(0,0)

    POINT_SIZE = 5

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
        painter.drawPoint(self._x,self._y)

    @staticmethod
    def computeTransformation(xo,yo,dx,dy,o):
        # xC = (xB - xO) * cos (β) + (yB - yO) * sin (β) + xO
        # yC = - (xB - xO) * sin(β) + (yB - yO) * cos(β) + yO
        a=-radians(o)
        return int(dx * cos(a) + dy * sin(a) + xo), int(-dx * sin(a) + dy * cos(a) + yo)

    def contains(self, point):
        return False