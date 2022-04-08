from typing import Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter
from discoverySimulator.representation.shapes import Shape, Rectangle
from math import radians, cos, sin


class Point(Shape):

    """ The Point class provides a point."""

    __POINT_SIZE = 5

    def __init__(self, color: str = "#000", opacity: int = 255):
        super().__init__(color, opacity)

    # GETTERS
    def getBoundingBox(self) -> Rectangle:
        """ Returns the bounding box of a point."""
        return Rectangle(self.__POINT_SIZE, self.__POINT_SIZE)

    def contains(self, point) -> bool:
        return False

    def getLineDecomposition(self):
        return []

    @staticmethod
    def computeTransformation(xo: float, yo: float, dx: float, dy: float, o: float) -> Tuple[float, float]:
        a = -radians(o)
        return round(dx * cos(a) + dy * sin(a) + xo,3),round(-dx * sin(a) + dy * cos(a) + yo,3)

    def paint(self, painter: QPainter):
        super().paint(painter)
        painter.setPen(QPen(self._color, self.__POINT_SIZE, Qt.SolidLine))
        painter.drawPoint(0, 0)

    def offset(self, value: float,truncated:bool=False) -> Rectangle:
        rec = Rectangle(self.__POINT_SIZE + 2 * value, self.__POINT_SIZE + 2 * value)
        rec.setPose(self._pose.copy())
        return rec
