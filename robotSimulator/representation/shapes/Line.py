from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPen, QColor
from . import Shape
from math import sin,cos, radians

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


    def getLineDecomposition(self):
        # ligne plutôt rectangle du fait de son épaisseur ?
        x1 = self._pose.getX()
        y1 = self._pose.getY()

        dx = 0
        dy = self._length
        a = -radians(self._pose.getOrientation())
        x2 = int(dx * cos(a) + dy * sin(a) + x1)
        y2 = int(-dx * sin(a) + dy * cos(a) + y1)

        return [QLineF(x1,y1,x2,y2)]
