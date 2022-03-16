from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPen
from . import Shape
from .Point import Point


class Line(Shape):

    def __init__(self,length,width,color,opacity=255):
        super().__init__(color,opacity)
        self._length=length
        self._width=width

    def paint(self,painter):
        super().paint(painter)
        # de quel façon dessiner une ligne : origine en 0 en x et y ou moitié en x et 0 en y ?
        painter.setPen(QPen(self._color, self._width, Qt.SolidLine))
        painter.drawLine(0,0,0,self._length) # ligne verticale

    def setLength(self,length):
        self._length=length

    @staticmethod
    def getLineCoefficient(line):
        a = (line.y2() - line.y1()) / (line.x2() - line.x1())
        b = line.y1()-a*line.x1()
        return a,b

    def getLineDecomposition(self):
        # ligne plutôt rectangle du fait de son épaisseur ?
        x1 = self._pose.getX()
        y1 = self._pose.getY()
        dx = 0
        dy = self._length
        x2,y2 = Point.computeTransformation(x1,y1,dx,dy,self._pose.getOrientation())

        return [QLineF(x1,y1,x2,y2)]

    def contains(self, point):
        return False
