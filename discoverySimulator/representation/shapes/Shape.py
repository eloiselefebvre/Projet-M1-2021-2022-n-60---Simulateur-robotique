from abc import ABC,abstractmethod
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QColor, QPen, QPainter

from .Border import Border
from ...Pose import Pose


class Shape(ABC):

    """ The Shape class provides ...."""

    _ORIENTATION_MARK_WIDTH = 2
    _ORIENTATION_MARK_LIGHTER_FACTOR = 160

    def __init__(self,color:str,opacity:int):
        self._color = QColor(color)
        self._opacity=opacity
        self._border=None
        self._pose=None

        self._orientationMark=False


    # SETTERS
    def setPose(self,pose:Pose):
        """ This method is used to change the position of a shape
        @param pose: the new position
        """
        self._pose=pose

    def setOpacity(self,opacity:int):
        """ This method is used to change the opacity of a shape
        @param opacity: the new opacity
        """
        self._opacity=opacity

    def setColor(self,color:str):
        """ This method is used to change the color of a shape
        @param color: the new color
        """
        self._color=QColor(color)

    # GETTERS
    def getPose(self) -> Pose:
        """ This method is used to get the position of a shape
        @return  The position of the shape
        """
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
        """ This method is used to get the color of a shape
        @return  The color of a shape
        """
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
        # intersection circle/circle
        if not shape1_lines and not shape2_lines:
            total_intersections.extend(self.getIntersectionWithCircle(shape))
        # intersection line/circle
        elif shape1_lines and not shape2_lines:
            for line in shape1_lines:
                intersections=shape.getIntersectionWithLine(line)
                if intersections:
                    total_intersections.extend(intersections)
        # intersection circle/line
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
        """ This method is used to get the bounding box of a shape
        """
        pass

    def addBorder(self, border:Border):
        """ This method is used to add a border on a shape
        @param border  The border to add
        """
        if isinstance(border, Border):
            self._border=border

    def removeBorder(self):
        """
        This method is used to remove a border on a shape
        @param border  The border to remove
        """
        self._border=None

    @abstractmethod
    def contains(self, point):
        pass

    @abstractmethod
    def offset(self,value:float,truncated:bool=False):
        pass

    def addOrientationMark(self):
        self._orientationMark = True

    def paintOrientationMark(self, painter):
        pass
