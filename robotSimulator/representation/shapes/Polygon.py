import random
from PyQt5.QtCore import Qt, QLineF, QPoint
from PyQt5.QtGui import QPolygon, QBrush

from robotSimulator.representation.shapes import Shape

class Polygon(Shape):

    POINT_SIZE = 5

    def __init__(self,points,color="#000",opacity=255):
        super().__init__(color,opacity)
        self._points=points
        # TODO: Convertir la liste de points en QPoint

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
        # https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
        pose = QPoint(self._pose.getX(), self._pose.getY())
        c=False
        j=len(self._points)-1
        for i in range(len(self._points)):
            previousEdge=self._points[j]+pose
            edge = self._points[i] + pose
            if ((edge.y() > point.y()) != (previousEdge.y() > point.y())) and (point.x() < (previousEdge.x() - edge.x()) * (point.y() - edge.y()) / (previousEdge.y() - edge.y()) + edge.x()):
                c=not c
            j=i
        return c

