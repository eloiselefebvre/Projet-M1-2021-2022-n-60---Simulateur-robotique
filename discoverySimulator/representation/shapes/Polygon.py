from __future__ import annotations
from typing import List, Tuple

from PyQt5.QtCore import Qt, QLineF, QPoint, QPointF
from PyQt5.QtGui import QPolygon, QBrush, QPainter, QPen, QColor
from discoverySimulator.representation.shapes import Shape, Rectangle

class Polygon(Shape):

    """ The Polygon class provides a polygon."""

    # TODO : Revoir la position des polygones comme le milieu de ses points

    def __init__(self,points:List[Tuple[int,int]],color:str=None,clockwise:bool=True,opacity:int=255):
        """ Constructs a Polygon.
        @param points  Points that determine the shape of the polygon
        @param color  Color of the shape
        @param opacity  Opacity of the shape"""
        super().__init__(color,opacity)
        self.__points=[QPoint(round(point[0]),round(point[1])) for point in points]
        self.__clockwise=clockwise

    # GETTERS
    def getBoundingBox(self) -> Rectangle:
        """ Returns the bounding box of a polygon."""
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

    def offset(self,value:float,truncated:bool=False) -> Polygon:
        # https://stackoverflow.com/questions/54033808/how-to-offset-polygon-edges
        points_offset=[]
        truncated_points_offset=[]
        points_number=len(self.__points)
        truncLines=[]

        value *= (1 if self.__clockwise else -1)
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

            l=value/(1+na.x()*nb.x()+na.y()*nb.y())**0.5

            p_prime = self.__points[curr] + 2**0.5 * l * bis
            points_offset.append((p_prime.x(),p_prime.y()))

            if truncated:
                if abs(l)>abs(value):
                    t=self.__points[curr] + value * bis
                    truncLines.append(QLineF(t.x(),t.y(),self.__points[curr].x(),self.__points[curr].y()).normalVector())
                else:
                    truncLines.append(None)

        if truncated:
            for curr in range(points_number):
                if truncLines[curr] is not None:
                    prev = (curr + points_number - 1) % points_number
                    next = (curr + 1) % points_number

                    lines=[QLineF(points_offset[prev][0],points_offset[prev][1],points_offset[curr][0],points_offset[curr][1]),
                           QLineF(points_offset[curr][0], points_offset[curr][1], points_offset[next][0],points_offset[next][1])]

                    for line in lines:
                        intersection = QPointF()
                        if line.intersect(truncLines[curr],intersection)==QLineF.UnboundedIntersection or line.intersect(truncLines[curr],intersection)==QLineF.BoundedIntersection:
                            truncated_points_offset.append((intersection.x(),intersection.y()))
                else:
                    truncated_points_offset.append(points_offset[curr])
            pol=Polygon(truncated_points_offset)
        else:
            pol=Polygon(points_offset)
        pol.setPose(self._pose.copy())
        return pol

    def paint(self, painter:QPainter):
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawPolygon(QPolygon(self.__points))



