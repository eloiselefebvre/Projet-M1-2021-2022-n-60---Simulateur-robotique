from abc import ABC,abstractmethod
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QColor, QPen, QPainter

from .Border import Border
from ...Pose import Pose


class Shape(ABC):

    ORIENTATION_MARK_WIDTH = 2
    ORIENTATION_MARK_LIGHTER_FACTOR = 160

    def __init__(self,color:str,opacity:int):
        self._color = QColor(color)
        self._opacity=opacity
        self._border=None
        self._pose=None

        self._orientationMark=False

    def addBorder(self,bord):
        if isinstance(bord,Border):
            self._border=bord

    def removeBorder(self):
        self._border=None

    # SETTERS
    def setPose(self,pose:Pose):
        self._pose=pose

    def setOpacity(self,opacity:int):
        self._opacity=opacity

    def setColor(self,color:str):
        self._color=QColor(color)

    # GETTERS
    def getPose(self):
        return self._pose

    def paint(self,painter:QPainter):
        painter.translate(self._pose.getX() + self._pose.getRotationCenterX(), self._pose.getY() + self._pose.getRotationCenterY())
        painter.rotate(self._pose.getOrientation())
        painter.translate(-self._pose.getRotationCenterX(), -self._pose.getRotationCenterY())
        self._color.setAlpha(self._opacity)
        if self._border is not None:
            painter.setPen(QPen(self._border.getColor(),self._border.getWidth(), Qt.SolidLine))
        else:
            painter.setPen(Qt.NoPen)

    def getColor(self):
        return self._color.name()

    @abstractmethod
    def getLineDecomposition(self):
        pass

    def getIntersectionsWith(self, shape):
        """
        3 cas possibles du fait de la décomposition en lignes :
        -> cercle vs cercle
        -> ligne vs ligne
        -> cercle vs ligne
        """
        from .Point import Point
        if isinstance(self,Point) or isinstance(shape,Point):
            return []

        total_intersections=[]
        shape1_lines = self.getLineDecomposition()
        shape2_lines = shape.getLineDecomposition()
        # intersection cercle/cercle
        if not shape1_lines and not shape2_lines:
            total_intersections.extend(self.getIntersectionWithCircle(shape))
        # intersection ligne/cercle
        elif shape1_lines and not shape2_lines:
            for line in shape1_lines:
                intersections=shape.getIntersectionWithLine(line)
                if intersections:
                    total_intersections.extend(intersections)
        # intersection cercle/ligne
        elif not shape1_lines and shape2_lines:
            for line in shape2_lines:
                intersections = self.getIntersectionWithLine(line)
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
    def getBoundingBox(self):
        pass

    @abstractmethod
    def contains(self, point):
        pass

    @abstractmethod
    def offset(self,value:float):
        pass

    def addOrientationMark(self):
        self._orientationMark = True

    def paintOrientationMark(self, painter):
        pass
