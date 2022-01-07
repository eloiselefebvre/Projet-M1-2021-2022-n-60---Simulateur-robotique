from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from Point import Point
from Representation import Representation

class Rectangle(Representation):

    def __init__(self, origin, width, height,orientation, color):
        Representation.__init__(self, origin,orientation, color)
        self._width = width
        self._height = height
        self._center = Point(self._origin.getX() + self._width / 2, self._origin.getY() + self._height / 2)

    def print(self):
        print("Rectangle - origin : ", self._origin, ", width = ", self._width, ", height = ", self._height, sep="")

    def draw(self, painter):
        painter.translate(self._center.getX(), self._center.getY())
        painter.rotate(self._orientation)
        painter.setPen(QPen(QColor(self._color), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(self._color), Qt.SolidPattern))
        painter.drawRoundedRect(QRect(0, 0, self._width, self._height), 6, 6)

        painter.setBrush(QBrush(QColor("#1C1E32"), Qt.SolidPattern))
        painter.setPen(QPen(QColor("#f3f3f3"), 2, Qt.SolidLine))
        painter.drawRoundedRect(QRect(0, 10, 8, 20), 2, 2)
        painter.drawRoundedRect(QRect(self._width-8, 10, 8, 20), 2, 2)