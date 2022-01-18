from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen

from robotSimulator.Shape import Shape

class Circle(Shape):

    def __init__(self,radius,color,borderWidth=0,borderColor=None,opacity=255):
        super().__init__(color,opacity,borderWidth,borderColor)
        self._radius=radius

    def paint(self,painter,center,orientation):
        super().paint(painter, center, orientation)
        qcolor = QColor(self._color)
        qcolor.setAlpha(self._opacity)
        painter.setPen(QPen(qcolor, 0, Qt.SolidLine))
        painter.setBrush(QBrush(qcolor, Qt.SolidPattern))
        painter.drawEllipse(-self._radius,-self._radius,self._radius*2,self._radius*2)