from robotSimulator.representation.shapes.Shape import Shape

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

class Line(Shape):

    def __init__(self,length,width,color,opacity=255):
        super().__init__(color,opacity)
        self._length=length
        self._width=width


    def paint(self,painter,origin,orientation):
        super().paint(painter, origin, orientation)
        painter.setPen(QPen(self._color, self._width, Qt.SolidLine))
        painter.drawLine(0,0,0,self._length) # ligne verticale


