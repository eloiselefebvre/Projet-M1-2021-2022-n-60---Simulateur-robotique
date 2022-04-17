from abc import ABC,abstractmethod
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QColor, QPen, QPainter

from .Border import Border
from ...Pose import Pose


class Shape(ABC):

    """ The Shape class provides a Shape."""

    _ORIENTATION_MARK_WIDTH = 2
    _ORIENTATION_MARK_LIGHTER_FACTOR = 160

    def __init__(self,color:str,opacity:int):
        """ Constructs a Shape."""
        self._color = QColor(color)
        self._opacity=opacity
        self._border=None
        self._pose=None
        self._orientationMark=False

    # SETTERS
    def setPose(self,pose:Pose):
        """ Sets the position of a shape.
        @param pose  the new position"""
        self._pose=pose

    def setOpacity(self,opacity:int):
        """ Sets the opacity of a shape.
        @param opacity  the new opacity 0-255"""
        self._opacity=opacity

    def setColor(self,color:str):
        """ Sets the color of a shape.
        @param color  the new color"""
        self._color=QColor(color)

    # GETTERS
    def getPose(self) -> Pose:
        """ Returns the position of a shape."""
        return self._pose

    def paint(self,painter:QPainter):
        painter.translate(self._pose.getX() + self._pose.getRotationCenterX(), self._pose.getY() + self._pose.getRotationCenterY())
        painter.rotate(self._pose.getOrientation())
        painter.translate(-self._pose.getRotationCenterX(), -self._pose.getRotationCenterY())
        self._color.setAlpha(self._opacity)
        if self._border is not None:
            pen=QPen(self._border.getColor(), self._border.getWidth(), Qt.SolidLine)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
        else:
            painter.setPen(Qt.NoPen)

    def getColor(self):
        """ Returns the color of a shape."""
        return self._color.name()

    @abstractmethod
    def getLineDecomposition(self):
        pass

    def getIntersectionsWith(self, shape):
        """
        3 possible cases due to the breakdown into lines:
        -> circle vs circle
        -> line vs line
        -> circle vs line
        """
        from .Point import Point
        if isinstance(self,Point) or isinstance(shape,Point):
            return []

        total_intersections=[]
        shape1_lines = self.getLineDecomposition()
        shape2_lines = shape.getLineDecomposition()
        # Intersection circle/circle
        if not shape1_lines and not shape2_lines:
            total_intersections.extend(self.getIntersectionWithCircle(shape))
        # Intersection line/circle
        elif shape1_lines and not shape2_lines:
            for line in shape1_lines:
                intersections=shape.getIntersectionWithLine(line)
                if intersections:
                    total_intersections.extend(intersections)

        # Intersection circle/line
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
        """ Returns the bounding box of a shape."""
        pass

    def addBorder(self, border:Border):
        """ Adds a border on a shape.
        @param border  The border to add"""
        if isinstance(border, Border):
            self._border=border

    def removeBorder(self):
        """
        Removes a border on a shape.
        @param border  The border to remove"""
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
