from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen

from robotSimulator.Border import Border

class Shape:
    def __init__(self,color,opacity):
        self._color = QColor(color)
        self._opacity=opacity
        self._border=None

    def addBorder(self,border):
        if isinstance(border,Border):
            self._border=border

    def paint(self,painter,origin,orientation):
        painter.translate(origin.getX(), origin.getY())
        painter.rotate(orientation)
        self._color.setAlpha(self._opacity)
        if self._border is not None:
            painter.setPen(QPen(self._border.getColor(),self._border.getWidth(), Qt.SolidLine))
        else:
            painter.setPen(Qt.NoPen)

    def setOpacity(self,opacity):
        self._opacity=opacity