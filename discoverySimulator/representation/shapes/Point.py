from typing import Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter
from discoverySimulator.representation.shapes import Shape, Rectangle
from math import radians, cos, sin


class Point(Shape):
    POINT_SIZE = 5

    def __init__(self, color: str = "#000", opacity: int = 255):
        super().__init__(color, opacity)

    # GETTERS
    def getBoundingBox(self) -> Rectangle:
        """
        This method is used to get the bounding box of a point
        :return: the bounding box of the point
        """
        return Rectangle(self.POINT_SIZE, self.POINT_SIZE)

    def contains(self, point) -> bool:
        return False

    def getLineDecomposition(self):
        return []

    @staticmethod
    def computeTransformation(xo: float, yo: float, dx: float, dy: float, o: float) -> Tuple[float, float]:
        a = -radians(o)
        return dx * cos(a) + dy * sin(a) + xo, -dx * sin(a) + dy * cos(a) + yo

    def paint(self, painter: QPainter):
        super().paint(painter)
        painter.setPen(QPen(self._color, self.POINT_SIZE, Qt.SolidLine))
        painter.drawPoint(0, 0)

    def offset(self, value: float) -> Rectangle:
        rec = Rectangle(self.POINT_SIZE + 2*value, self.POINT_SIZE + 2*value)
        rec.setPose(self._pose.copy())
        return rec
