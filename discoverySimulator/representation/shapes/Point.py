from typing import Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter
from discoverySimulator.representation.shapes import Shape, Rectangle
from math import radians, cos, sin

class Point(Shape):

    POINT_SIZE = 5

    def __init__(self,color:str="#000",opacity:int=255):
        super().__init__(color,opacity)

    def getBoundingBox(self) -> Rectangle:
        return Rectangle(self.POINT_SIZE, self.POINT_SIZE)

    def contains(self, point) -> bool:
        return False

    def getLineDecomposition(self):
        return []

    @staticmethod
    def computeTransformation(xo:float,yo:float,dx:float,dy:float,o:float) -> Tuple[float,float]:
        # xC = (xB - xO) * cos (β) + (yB - yO) * sin (β) + xO
        # yC = - (xB - xO) * sin(β) + (yB - yO) * cos(β) + yO
        a=-radians(o)
        return dx * cos(a) + dy * sin(a) + xo, -dx * sin(a) + dy * cos(a) + yo

    def paint(self,painter:QPainter):
        super().paint(painter)
        painter.setPen(QPen(self._color, self.POINT_SIZE, Qt.SolidLine))
        painter.drawPoint(0,0)