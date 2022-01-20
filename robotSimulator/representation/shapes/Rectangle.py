from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPen, QBrush
from robotSimulator.config import *

from robotSimulator.representation.shapes.Shape import Shape

class Rectangle(Shape):
    def __init__(self,width,height,color,borderRadius=0,opacity=255):
        super().__init__(color,opacity)
        self._width=width
        self._height=height
        self._borderRadius=borderRadius
        self._orientationMark = True

    def removeOrientationMark(self):
        self._orientationMark=False

    def paint(self,painter,origin,orientation):
        super().paint(painter,origin,orientation)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawRoundedRect(QRect(-int(self._width/2),-int(self._height/2), self._width, self._height),self._borderRadius,self._borderRadius) # dessiné à partir du center
        if self._orientationMark:
            self.paintOrientationMark(painter)

    def paintOrientationMark(self,painter):
        painter.setPen(QPen(self._color.lighter(ORIENTATION_MARK_LIGHTER_FACTOR),ORIENTATION_MARK_WIDTH, Qt.SolidLine))
        widthToCompensate = ORIENTATION_MARK_WIDTH if self._border is None else max(ORIENTATION_MARK_WIDTH,self._border.getWidth())
        ypos = int(self._height / 2  * 8/10)
        painter.drawLine(widthToCompensate - int(self._width / 2), ypos, int(self._width / 2) - widthToCompensate, ypos)