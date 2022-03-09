import random
from PyQt5.QtCore import Qt, QLineF, QPoint
from PyQt5.QtGui import QPolygon, QBrush

from robotSimulator.representation.shapes import Shape

class Polygon(Shape):

    POINT_SIZE = 5

    def __init__(self,points,color="#000",opacity=255):
        super().__init__(color,opacity)
        self._points=points

    def paint(self, painter):
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawPolygon(QPolygon(self._points))

    def getLineDecomposition(self):
        lines=[]
        pose = QPoint(self._pose.getX(),self._pose.getY())
        for i in range (len(self._points)):
            if i>0:
                lines.append(QLineF(self._points[i-1]+pose,self._points[i]+pose))
        return lines

    def contains(self, point):
        for line in self.getLineDecomposition():
            d = (line.x2() - line.x1()) * (point.y() - line.y1()) - (line.y2() - line.y1()) * (point.x() - line.x1())
            if not d < 0:  # point à droite de la ligne (pas bon car sens trigonométrique)
                return False
        return True
