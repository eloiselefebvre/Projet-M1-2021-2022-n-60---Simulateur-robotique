from typing import List, Tuple

from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPen, QPainter
from . import Shape, Rectangle
from .Point import Point


class Line(Shape):

    """ The Line class provides ...."""

    def __init__(self,length:float,width:float,color:str=None,opacity:int=255):
        super().__init__(color,opacity)
        self.__length=length
        self.__width=width

    # SETTERS
    def setLength(self,length:float):
        """ This method is used to change the length of a line
        @param length  Length of the line [px]
        """
        self.__length=length

    # GETTERS
    @staticmethod
    def getLineCoefficient(line: QLineF) -> Tuple[float, float]:
        a = (line.y2() - line.y1()) / (line.x2() - line.x1())
        b = line.y1() - a * line.x1()
        return a, b

    def getBoundingBox(self) -> Rectangle:
        """ This method is used to get the bounding box of a rectangle
        @return  The bounding box of the rectangle
        """
        return Rectangle(self.__width, self.__length)

    def contains(self, point) -> bool:
        return False

    def getLineDecomposition(self) -> List[QLineF]:
        x1 = self._pose.getX()
        y1 = self._pose.getY()
        dx = 0
        dy = self.__length
        x2,y2 = Point.computeTransformation(x1,y1,dx,dy,self._pose.getOrientation())

        return [QLineF(x1,y1,x2,y2)]

    def offset(self,value:float,truncated:bool=False) -> Rectangle:
        rec = Rectangle(self.__width + 2 * value, self.__length + 2 * value)
        pose=self._pose.copy()
        dx,dy=Point.computeTransformation(pose.getX(), pose.getY(), 0, self.__length / 2, pose.getOrientation())
        pose.move(dx,dy)
        rec.setPose(pose)
        return rec

    def paint(self,painter:QPainter):
        super().paint(painter)
        painter.setPen(QPen(self._color, self.__width, Qt.SolidLine))
        painter.drawLine(0, 0, 0, round(self.__length))