from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPen, QBrush
from . import Shape

class Rectangle(Shape):

    ORIENTATION_MARK_WIDTH = 2
    ORIENTATION_MARK_LIGHTER_FACTOR = 160

    def __init__(self,width,height,color,borderRadius=0,opacity=255):
        super().__init__(color,opacity)
        self._width=width
        self._height=height
        self._borderRadius=borderRadius
        self._orientationMark = True

    def removeOrientationMark(self):
        self._orientationMark=False

    def paint(self,painter,pose):
        super().paint(painter,pose)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawRoundedRect(QRect(-int(self._width/2),-int(self._height/2), self._width, self._height),self._borderRadius,self._borderRadius) # dessiné à partir du center
        if self._orientationMark:
            self.paintOrientationMark(painter)

    def paintOrientationMark(self,painter):
        painter.setPen(QPen(self._color.lighter(self.ORIENTATION_MARK_LIGHTER_FACTOR),self.ORIENTATION_MARK_WIDTH, Qt.SolidLine))
        widthToCompensate = self.ORIENTATION_MARK_WIDTH if self._border is None else max(self.ORIENTATION_MARK_WIDTH,self._border.getWidth())
        ypos = int(self._height / 2  * 8/10)
        painter.drawLine(widthToCompensate - int(self._width / 2), ypos, int(self._width / 2) - widthToCompensate, ypos)