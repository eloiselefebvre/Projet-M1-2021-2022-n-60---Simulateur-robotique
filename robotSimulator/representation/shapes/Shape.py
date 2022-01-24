from abc import ABC
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen
from . import Border

class Shape(ABC):
    def __init__(self,color,opacity):
        self._color = QColor(color)
        self._opacity=opacity
        self._border=None

    def addBorder(self,bord):
        #print("Border",type(Border))
        #if isinstance(bord,Border):
        #    self._border=bord
        self._border = bord

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