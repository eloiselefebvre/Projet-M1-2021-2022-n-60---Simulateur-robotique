from PyQt5.QtCore import QRect, Qt, QLine, QLineF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor
from . import Shape
from robotSimulator.representation.shapes.Line import Line

from math import sin,cos, radians

class Rectangle(Shape):

    ORIENTATION_MARK_WIDTH = 2
    ORIENTATION_MARK_LIGHTER_FACTOR = 160

    def __init__(self,width,height,color,borderRadius=0,opacity=255):
        super().__init__(color,opacity)
        self._width=width
        self._height=height
        self._borderRadius=borderRadius
        self._orientationMark = True

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def removeOrientationMark(self):
        self._orientationMark=False

    def paint(self,painter):
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawRoundedRect(QRect(-int(self._width / 2), -int(self._height / 2), self._width, self._height),self._borderRadius,self._borderRadius) # dessiné à partir du center
        if self._orientationMark:
            self.paintOrientationMark(painter)

    def paintOrientationMark(self,painter):
        painter.setPen(QPen(self._color.lighter(self.ORIENTATION_MARK_LIGHTER_FACTOR),self.ORIENTATION_MARK_WIDTH, Qt.SolidLine))
        widthToCompensate = self.ORIENTATION_MARK_WIDTH if self._border is None else max(self.ORIENTATION_MARK_WIDTH,self._border.getWidth())
        ypos = int(self._height / 2  * 8/10)
        painter.drawLine(widthToCompensate - int(self._width / 2), ypos, int(self._width / 2) - widthToCompensate, ypos)

    def getLineDecomposition(self):
        # xC = (xB - xO) * cos (β) + (yB - yO) * sin (β) + xO
        # yC = - (xB - xO) * sin(β) + (yB - yO) * cos(β) + yO

        lines=[]
        w = self._width / 2
        h = self._height / 2
        sign = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        pts = []
        x0 = self._pose.getX() + self._pose.getRotX()
        y0 = self._pose.getY() + self._pose.getRotY()
        for i in range(4):
            x = self._pose.getX() + sign[i][0] * w
            y = self._pose.getY() + sign[i][1] * h
            dx = x - x0
            dy = y - y0
            a = -radians(self._pose.getOrientation())
            nx = int(dx * cos(a) + dy * sin(a) + x0)
            ny = int(-dx * sin(a) + dy * cos(a) + y0)
            pts.append((nx, ny))
        pts.append(pts[0])

        for i in range(4):
            lines.append(QLineF(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]))
        return lines