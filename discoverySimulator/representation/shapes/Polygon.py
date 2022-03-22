from PyQt5.QtCore import Qt, QLineF, QPoint, QPointF
from PyQt5.QtGui import QPolygon, QBrush, QPen, QColor

from discoverySimulator.representation.shapes import Shape, Rectangle


class Polygon(Shape):

    POINT_SIZE = 5

    def __init__(self,points,color=None,opacity=255):
        super().__init__(color,opacity)
        self._points=[QPoint(point[0],point[1]) for point in points]

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

    def offset(self,value): # sens horaire
        # https://stackoverflow.com/questions/54033808/how-to-offset-polygon-edges
        points_offset=[]
        points_number=len(self._points)
        for curr in range(points_number):
            prev = (curr + points_number - 1) % points_number
            next = (curr + 1) % points_number

            line1 = QLineF(self._points[prev].x(),self._points[prev].y(),self._points[curr].x(),self._points[curr].y())
            line2 = QLineF(self._points[curr].x(),self._points[curr].y(),self._points[next].x(),self._points[next].y())
            line1_normal=line1.normalVector()
            line2_normal=line2.normalVector()

            na = QPointF(line1_normal.x2()-line1_normal.x1(),line1_normal.y2()-line1_normal.y1())
            na/=line1_normal.length()

            nb = QPointF(line2_normal.x2()-line2_normal.x1(),line2_normal.y2()-line2_normal.y1())
            nb/=line2_normal.length()

            bis=na+nb
            length_bis = (bis.x()**2+bis.y()**2)**0.5
            bis/=length_bis

            l=value/(1+na.x()*nb.x()+na.y()*nb.y())**0.5

            p_prime = self._points[curr]+l*bis
            points_offset.append((round(p_prime.x()),round(p_prime.y())))

        pol=Polygon(points_offset)
        pol.setPose(self._pose.copy())
        return pol
