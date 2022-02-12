from abc import ABC
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen

class Shape:
    def __init__(self,color,opacity):
        self._color = QColor(color)
        self._opacity=opacity
        self._border=None
        self._pose=None

    def addBorder(self,bord):
        #print("Border",type(Border))
        #if isinstance(bord,Border):
        #    self._border=bord
        self._border = bord

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

    def isCollidedWith(self,shape):
        pass