from typing import List

from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPen
from . import Shape, Rectangle
from .Point import Point

from typing import Tuple

class Line(Shape):

    def __init__(self,length:float,width:float,color:str,opacity:int=255):
        super().__init__(color,opacity)
        self._length=length
        self._width=width

    def paint(self,painter):
        super().paint(painter)
        painter.setPen(QPen(self._color, self._width, Qt.SolidLine))
        painter.drawLine(0,0,0,self._length) # vertical line

    def setLength(self,length:float):
        """
        This method is used to change the length of a line
        :param length: length of the line [px]
        """
        self._length=length

    @staticmethod
    def getLineCoefficient(line:QLineF) -> Tuple[float,float]:
        a = (line.y2() - line.y1()) / (line.x2() - line.x1())
        b = line.y1()-a*line.x1()
        return a,b

    def getLineDecomposition(self) -> List[QLineF]:
        x1 = self._pose.getX()
        y1 = self._pose.getY()
        dx = 0
        dy = self._length
        x2,y2 = Point.computeTransformation(x1,y1,dx,dy,self._pose.getOrientation())

        return [QLineF(x1,y1,x2,y2)]

    def contains(self, point) -> bool:
        return False

    def offset(self,value:float) -> Rectangle:
        rec = Rectangle(self._width+value,self._length+value)
        pose=self._pose.copy()
        dx,dy=Point.computeTransformation(pose.getX(),pose.getY(),0,self._length/2,pose.getOrientation())
        pose.move(dx,dy)
        rec.setPose(pose)
        return rec

    def getBoundingBox(self) -> Rectangle:
        return Rectangle(self._width,self._length)
