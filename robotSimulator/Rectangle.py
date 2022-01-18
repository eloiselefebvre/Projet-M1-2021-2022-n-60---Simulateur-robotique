from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPen, QBrush, QColor
from robotSimulator.config import *

from robotSimulator.Shape import Shape

class Rectangle(Shape):
    def __init__(self,width,height,color,borderRadius=0,opacity=255):
        super().__init__(color,opacity)
        self._width=width
        self._height=height
        self._borderRadius=borderRadius

    def paint(self,painter,center,orientation):
        super().paint(painter,center,orientation)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawRoundedRect(QRect(-int(self._width/2),-int(self._height/2), self._width, self._height),self._borderRadius,self._borderRadius) # last parameters for border radius
        self.paintOrientationMark(painter)

    def paintOrientationMark(self,painter):
        painter.setPen(QPen(self._color.lighter(ORIENTATION_MARK_LIGHTER_FACTOR),ORIENTATION_MARK_WIDTH, Qt.SolidLine))
        widthToCompensate = ORIENTATION_MARK_WIDTH if self._border is None else max(ORIENTATION_MARK_WIDTH,self._border.getWidth())
        painter.drawLine(widthToCompensate - int(self._width / 2), int(self._height / 2) - ORIENTATION_MARK_DISTANCE_FROM_FRONT, int(self._width / 2) - widthToCompensate, int(self._height / 2) - ORIENTATION_MARK_DISTANCE_FROM_FRONT)  # if self._borderWidth==0 else border