from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from discoverySimulator.representation.shapes import Shape, Rectangle
from math import radians, cos, sin

class Point(Shape):

    POINT_SIZE = 5

    def __init__(self,color="#000",opacity=255):
        super().__init__(color,opacity)

    def getLineDecomposition(self):
        return []

    def paint(self,painter):
        super().paint(painter)
        painter.setPen(QPen(self._color, self.POINT_SIZE, Qt.SolidLine))
        painter.drawPoint(0,0)

    @staticmethod
    def computeTransformation(xo,yo,dx,dy,o):
        # xC = (xB - xO) * cos (β) + (yB - yO) * sin (β) + xO
        # yC = - (xB - xO) * sin(β) + (yB - yO) * cos(β) + yO
        a=-radians(o)
        return int(dx * cos(a) + dy * sin(a) + xo), int(-dx * sin(a) + dy * cos(a) + yo)

    def contains(self, point):
        return False

    def getBoundingBox(self):
        return Rectangle(self.POINT_SIZE, self.POINT_SIZE)