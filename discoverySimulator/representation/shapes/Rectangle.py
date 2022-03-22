from typing import List

from PyQt5.QtCore import QRect, Qt, QLineF
from PyQt5.QtGui import QPen, QBrush, QPainter
from . import Shape
from .Point import Point

class Rectangle(Shape):

    ORIENTATION_MARK_WIDTH = 2
    ORIENTATION_MARK_LIGHTER_FACTOR = 160

    def __init__(self,width:float,height:float,color:str=None,borderRadius:int=0,opacity:int=255):
        """
        This method allows to create a Rectangle
        :param width: width of the rectangle [px]
        :param height: height of the rectangle [px]
        :param color: color of the shape
        :param borderRadius: borderRadius of the rectangle [px]
        :param opacity: opacity of the shape
        """
        super().__init__(color,opacity)
        self._width=width
        self._height=height
        self._borderRadius=int(borderRadius)
        self._orientationMark = False
        self._rect=QRect(-int(self._width / 2), -int(self._height / 2), int(self._width), int(self._height))

    # GETTERS
    def getWidth(self) -> float:
        """
        This method is used to get the width of a rectangle
        :return: width of the rectangle [px]
        """
        return self._width

    def getHeight(self) -> float:
        """
        This method is used to get the height of a rectangle
        :return: height of the rectangle [px]
        """
        return self._height

    def getBoundingBox(self):
        return self

    def getLineDecomposition(self) -> List[QLineF]:
        lines=[]
        w = self._width / 2
        h = self._height / 2
        sign = [(-1, -1), (-1, 1), (1, 1), (1, -1)] # sens trigonométrique
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
            if not d<0: # point à droite de la ligne (pas bon car sens trigonométrique)
                return False
        return True

    def addOrientationMark(self):
        self._orientationMark=True

    def offset(self,value:float):
        rectangle = Rectangle(self._width+value,self._height+value,self._color)
        rectangle.setPose(self._pose)
        return rectangle

    def paint(self,painter:QPainter):
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawRoundedRect(self._rect,self._borderRadius,self._borderRadius) # dessiné à partir du center
        if self._orientationMark:
            self.paintOrientationMark(painter)

    def paintOrientationMark(self,painter):
        painter.setPen(QPen(self._color.lighter(self.ORIENTATION_MARK_LIGHTER_FACTOR),self.ORIENTATION_MARK_WIDTH, Qt.SolidLine))
        widthToCompensate = self.ORIENTATION_MARK_WIDTH if self._border is None else max(self.ORIENTATION_MARK_WIDTH,self._border.getWidth())
        ypos = int(self._height / 2  * 8/10)
        painter.drawLine(widthToCompensate - int(self._width / 2), ypos, int(self._width / 2) - widthToCompensate, ypos)