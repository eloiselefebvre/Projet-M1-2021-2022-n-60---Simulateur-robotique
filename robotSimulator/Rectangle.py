from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPen, QBrush, QColor

from robotSimulator.Shape import Shape

class Rectangle(Shape):
    def __init__(self,width,height,color,borderRadius=0,borderWidth=0,borderColor=None,opacity=255):
        super().__init__(color,opacity,borderWidth,borderColor)
        self._width=width
        self._height=height
        self._borderRadius=borderRadius

    def paint(self,painter,center,orientation):
        super().paint(painter,center,orientation)
        qcolor = QColor(self._color)
        qcolor.setAlpha(self._opacity)
        painter.setPen(QPen(QColor(self._borderColor),self._borderWidth, Qt.SolidLine))
        painter.setBrush(QBrush(qcolor, Qt.SolidPattern))
        painter.drawRoundedRect(QRect(-int(self._width/2),-int(self._height/2), self._width, self._height),self._borderRadius,self._borderRadius) # last parameters for border radius
        yline = 6
        border = 3
        painter.setPen(QPen(qcolor.lighter(160),border, Qt.SolidLine))
        painter.drawLine(border-int(self._width/2),int(self._height/2)-yline,int(self._width/2)-border,int(self._height/2)-yline) # if self._borderWidth==0 else border