from abc import ABC
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QColor, QPen

class Shape(ABC):
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

    def isCollidedWith(self, shape):
        # intersection cercle/cercle
        if not hasattr(self,'getLineDecomposition') and not hasattr(shape,'getLineDecomposition'):
            return ((self._pose.getX()-shape.getPose().getX())**2 + (self._pose.getY()-shape.getPose().getY())**2)**0.5 < self._radius+shape.getRadius()
        # intersection ligne/cercle
        elif hasattr(self,'getLineDecomposition') and not hasattr(shape,'getLineDecomposition'):
            lines=self.getLineDecomposition()
            for line in lines:
                if shape.isIntersectionWithLine(line):
                    return True
            return False
        # intersection cercle/ligne
        elif not hasattr(self,'getLineDecomposition') and hasattr(shape, 'getLineDecomposition'):
            return False
        else:
            r1_lines = self.getLineDecomposition()
            r2_lines=shape.getLineDecomposition()
            for r1_line in r1_lines:
                for r2_line in r2_lines:
                    if r1_line.intersect(r2_line,QPointF())==QLineF.BoundedIntersection:
                        return True
            return False


"""
rect vs rect
rect vs line
line vs line
circle vs circle
circle vs rect
circle vs line

-> cercle vs cercle
-> ligne vs ligne
-> cercle vs ligne

"""
