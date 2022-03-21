from PyQt5.QtCore import Qt, QLineF, QPoint
from PyQt5.QtGui import QPolygon, QBrush

from discoverySimulator.representation.shapes import Shape, Rectangle


class Polygon(Shape):

    POINT_SIZE = 5

    def __init__(self,points,color=None,opacity=255):
        super().__init__(color,opacity)
        self._points=points

        for i in range (len(self._points)):
            self._points[i]=QPoint(self._points[i][0],self._points[i][1])

    def paint(self, painter):
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawPolygon(QPolygon(self._points))

    def getLineDecomposition(self):
        lines=[]
        pose = QPoint(self._pose.getX(),self._pose.getY())
        points_number=len(self._points)
        for i in range (1,points_number+1):
            lines.append(QLineF(self._points[i-1]+pose,self._points[i if i<points_number else 0]+pose))
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

    def getBoundingBox(self):
        min_x=self._points[0].x()
        min_y = self._points[0].y()
        max_x=self._points[0].x()
        max_y = self._points[0].y()

        for point in self._points:
            if point.x()<min_x:
                min_x=point.x()
            if point.y()<min_y:
                min_y = point.y()
            if point.x()>max_x:
                max_x = point.x()
            if point.y()>max_y:
                max_y=point.y()
        return Rectangle(max_x-min_x,max_y-min_y)
