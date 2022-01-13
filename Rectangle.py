from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPen, QBrush, QColor

from Shape import Shape

class Rectangle(Shape):
    def __init__(self,width,height,color,borderRadius=0,borderWidth=0,borderColor=None,opacity=255):
        super().__init__(color,opacity,borderWidth,borderColor)
        self._width=width
        self._height=height
        self._borderRadius=borderRadius

    def paint(self,painter,x,y,orientation):
        painter.translate(x,y)
        painter.rotate(orientation) # rotation depuis un angle, à changer depuis son center, cf bounding box
        qcolor = QColor(self._color)
        qcolor.setAlpha(self._opacity)
        painter.setPen(QPen(QColor(self._borderColor),self._borderWidth, Qt.SolidLine))
        painter.setBrush(QBrush(qcolor, Qt.SolidPattern))
        painter.drawRoundedRect(QRect(0, 0, self._width, self._height),self._borderRadius,self._borderRadius) # last parameters for border radius
        yline = 6
        border = 3
        painter.setPen(QPen(qcolor.lighter(160),border, Qt.SolidLine))
        painter.drawLine(border,self._height-yline,self._width-border,self._height-yline) # if self._borderWidth==0 else border
