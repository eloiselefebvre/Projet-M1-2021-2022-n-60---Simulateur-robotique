from typing import List, Tuple

from PyQt5.QtCore import Qt, QLineF, QPoint, QPointF
from PyQt5.QtGui import QPolygon, QBrush, QPen, QColor, QPainter

from discoverySimulator.representation.shapes import Shape, Rectangle


class Polygon(Shape):

    POINT_SIZE = 5

    def __init__(self,points:List[Tuple],color:str=None,clockwise:bool=True,opacity:int=255):
        """
        This method is used to create a Polygon
        :param points: points that determine the shape of the polygon
        :param color: color of the shape
        :param opacity: opacity of the shape
        """
        super().__init__(color,opacity)
        self.__points=[QPoint(point[0], point[1]) for point in points]
        self.__clockwise=clockwise

    # GETTERS
    def getBoundingBox(self) -> Rectangle:
        min_x=self.__points[0].x()
        min_y = self.__points[0].y()
        max_x=self.__points[0].x()
        max_y = self.__points[0].y()

        for point in self.__points:
            if point.x()<min_x:
                min_x=point.x()
            if point.y()<min_y:
                min_y = point.y()
            if point.x()>max_x:
                max_x = point.x()
            if point.y()>max_y:
                max_y=point.y()
        return Rectangle(max_x-min_x,max_y-min_y)

    def contains(self, point) -> bool:
        # https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
        pose = QPoint(self._pose.getX(), self._pose.getY())
        c=False
        j= len(self.__points) - 1
        for i in range(len(self.__points)):
            previousEdge= self.__points[j] + pose
            edge = self.__points[i] + pose
            if ((edge.y() > point.y()) != (previousEdge.y() > point.y())) and (point.x() < (previousEdge.x() - edge.x()) * (point.y() - edge.y()) / (previousEdge.y() - edge.y()) + edge.x()):
                c=not c
            j=i
        return c

    def getLineDecomposition(self) -> List[QLineF]:
        lines=[]
        pose = QPoint(self._pose.getX(),self._pose.getY())
        points_number=len(self.__points)
        for i in range (1,points_number+1):
            lines.append(QLineF(self.__points[i - 1] + pose, self.__points[i if i < points_number else 0] + pose))
        return lines

    def offset(self,value:float):
        # https://stackoverflow.com/questions/54033808/how-to-offset-polygon-edges
        points_offset=[]
        points_number=len(self.__points)
        for curr in range(points_number):
            prev = (curr + points_number - 1) % points_number
            next = (curr + 1) % points_number

            line1 = QLineF(self.__points[prev].x(), self.__points[prev].y(), self.__points[curr].x(), self.__points[curr].y())
            line2 = QLineF(self.__points[curr].x(), self.__points[curr].y(), self.__points[next].x(), self.__points[next].y())
            line1_normal=line1.normalVector()
            line2_normal=line2.normalVector()

            na = QPointF(line1_normal.x2()-line1_normal.x1(),line1_normal.y2()-line1_normal.y1())
            na/=line1_normal.length()

            nb = QPointF(line2_normal.x2()-line2_normal.x1(),line2_normal.y2()-line2_normal.y1())
            nb/=line2_normal.length()

            bis=na+nb
            length_bis = (bis.x()**2+bis.y()**2)**0.5
            bis/=length_bis

            l=(1 if self.__clockwise else -1)*value/(1+na.x()*nb.x()+na.y()*nb.y())**0.5

            p_prime = self.__points[curr] + l * bis
            points_offset.append((round(p_prime.x()),round(p_prime.y())))

        pol=Polygon(points_offset)
        pol.setPose(self._pose.copy())
        return pol

    def paint(self, painter:QPainter):
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawPolygon(QPolygon(self.__points))


