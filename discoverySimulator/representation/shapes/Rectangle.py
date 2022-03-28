from __future__ import annotations
from typing import List

from PyQt5.QtCore import QRect, Qt, QLineF
from PyQt5.QtGui import QPen, QBrush, QPainter
from . import Shape
from .Point import Point

class Rectangle(Shape):

    """ The Rectangle class provides ...."""

    def __init__(self,width:float,height:float,color:str=None,borderRadius:float=0,opacity:int=255):
        """ This method allows to create a Rectangle
        @param width  Width of the rectangle [px]
        @param height  Height of the rectangle [px]
        @param color  Color of the shape
        @param borderRadius  BorderRadius of the rectangle [px]
        @param opacity  Opacity of the shape
        """
        super().__init__(color,opacity)
        self.__width=width
        self.__height=height
        self.__borderRadius=int(borderRadius)
        self._rect=QRect(-int(self.__width / 2), -int(self.__height / 2), int(self.__width), int(self.__height))

    # GETTERS
    def getWidth(self) -> float:
        """ This method is used to get the width of a rectangle
        @return  Width of the rectangle [px]
        """
        return self.__width

    def getHeight(self) -> float:
        """ This method is used to get the height of a rectangle
        @return  Height of the rectangle [px]
        """
        return self.__height

    def getBoundingBox(self) -> Rectangle:
        """ This method is used to get the bounding box of a rectangle
        @return  The bounding box of the rectangle
        """
        return self

    def getLineDecomposition(self) -> List[QLineF]:
        lines=[]
        w = self.__width / 2
        h = self.__height / 2
        sign = [(-1, -1), (-1, 1), (1, 1), (1, -1)] # counterclockwise
        pts = []
        xo = self._pose.getX() + self._pose.getRotationCenterX()
        yo = self._pose.getY() + self._pose.getRotationCenterY()
        for i in range(4):
            x = self._pose.getX() + sign[i][0] * w
            y = self._pose.getY() + sign[i][1] * h
            dx = x - xo
            dy = y - yo
            pts.append(Point.computeTransformation(xo,yo,dx,dy,self._pose.getOrientation()))
        pts.append(pts[0])

        for i in range(4):
            lines.append(QLineF(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]))
        return lines


    def contains(self, point) -> bool:
        for line in self.getLineDecomposition():
            d = (line.x2()-line.x1())*(point.y()-line.y1())-(line.y2()-line.y1())*(point.x()-line.x1())
            if not d<0: # point to the right of the line (not good because trigonometric direction)
                return False
        return True

    def offset(self,value:float,truncated:bool=False) -> Rectangle:
        rectangle = Rectangle(self.__width + 2 * value, self.__height + 2 * value, self._color)
        rectangle.setPose(self._pose)
        return rectangle

    def paint(self,painter:QPainter):
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawRoundedRect(self._rect, self.__borderRadius, self.__borderRadius) # draw from the center
        if self._orientationMark:
            self.paintOrientationMark(painter)

    def paintOrientationMark(self,painter):
        painter.setPen(QPen(self._color.lighter(Shape._ORIENTATION_MARK_LIGHTER_FACTOR), Shape._ORIENTATION_MARK_WIDTH, Qt.SolidLine))
        widthToCompensate = Shape._ORIENTATION_MARK_WIDTH if self._border is None else max(Shape._ORIENTATION_MARK_WIDTH, self._border.getWidth())
        ypos = int(self.__height / 2 * 8 / 10)
        painter.drawLine(widthToCompensate - int(self.__width / 2), ypos, int(self.__width / 2) - widthToCompensate, ypos)