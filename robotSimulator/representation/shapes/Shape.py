from abc import ABC,abstractmethod
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QColor, QPen

from .Border import Border

class Shape(ABC):
    def __init__(self,color,opacity):
        self._color = QColor(color)
        self._opacity=opacity
        self._border=None
        self._pose=None

    def addBorder(self,bord):
        if isinstance(bord,Border):
            self._border=bord

    def removeBorder(self):
        self._border=None

    def setPose(self,pose):
        self._pose=pose

    def getPose(self):
        return self._pose

    def paint(self,painter):
        painter.translate(self._pose.getX()+self._pose.getRotX(),self._pose.getY()+self._pose.getRotY())
        painter.rotate(self._pose.getOrientation())
        painter.translate(-self._pose.getRotX(),-self._pose.getRotY())
        self._color.setAlpha(self._opacity)
        if self._border is not None:
            painter.setPen(QPen(self._border.getColor(),self._border.getWidth(), Qt.SolidLine))
        else:
            painter.setPen(Qt.NoPen)

    def setOpacity(self,opacity):
        self._opacity=opacity

    @abstractmethod
    def getLineDecomposition(self):
        pass

    def isCollidedWith(self, shape):
        """
        3 cas possibles du fait de la décomposition en lignes :
        -> cercle vs cercle
        -> ligne vs ligne
        -> cercle vs ligne
        """
        total_intersections=[]
        shape1_lines = self.getLineDecomposition()
        shape2_lines = shape.getLineDecomposition()
        # TODO : Gérer le cas du point (getLineDecomposition() renvoie [] comme pour le cercle)
        # intersection cercle/cercle
        if not shape1_lines and not shape2_lines:
            return ((self._pose.getX()-shape.getPose().getX())**2 + (self._pose.getY()-shape.getPose().getY())**2)**0.5 < self._radius+shape.getRadius()
        # intersection ligne/cercle
        elif shape1_lines and not shape2_lines:
            for line in shape1_lines:
                intersections=shape.isIntersectionWithLine(line)
                if intersections:
                    total_intersections.extend(intersections)
        # intersection cercle/ligne
        elif not shape1_lines and shape2_lines:
            for line in shape2_lines:
                intersections = self.isIntersectionWithLine(line)
                if intersections:
                    total_intersections.extend(intersections)
        else:
            for r1_line in shape1_lines:
                for r2_line in shape2_lines:
                    intersection = QPointF()
                    if r1_line.intersect(r2_line,intersection)==QLineF.BoundedIntersection:
                        total_intersections.append(intersection)
        return total_intersections

    @abstractmethod
    def contains(self, point):
        pass