from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QBrush, QPen, QColor
from . import Shape

class Circle(Shape):

    def __init__(self,radius,color,opacity=255):
        super().__init__(color,opacity)
        self._radius=radius

    def getRadius(self):
        return self._radius

    def paint(self,painter):
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawEllipse(-self._radius,-self._radius,self._radius*2,self._radius*2) # dessiné à partir du center

    def getLineDecomposition(self):
        return []

    def isIntersectionWithLine(self,line):
        intersections = []
        if line.x2()!=line.x1(): # pas ligne verticale
            a_line=(line.y2()-line.y1())/(line.x2()-line.x1())
            b_line=line.y1()-a_line*line.x1()

            A = 1+a_line**2
            B = -2*self._pose.getX()+2*a_line*(b_line-self._pose.getY())
            C = self._pose.getX()**2 + (b_line-self._pose.getY())**2 - self._radius**2

            delta = B**2-4*A*C
            if delta>=0:
                max_x = line.x2() if line.x2() > line.x1() else line.x1()
                min_x = line.x2() if line.x2() < line.x1() else line.x1()

                x1=(-B-delta**0.5)/(2*A)
                x2=(-B+delta**0.5)/(2*A)
                # x1 = x2 si droite tangente au cercle
                y1=a_line*x1+b_line
                y2 = a_line * x2 + b_line

                if x1>=min_x and x1<=max_x:
                    intersections.append(QPointF(x1,y1))
                if x2>=min_x and x2<=max_x: # appartient au segment
                    intersections.append(QPointF(x2, y2))
        else: # ligne verticale
            A=1
            B=-2*self.getPose().getY()
            C=self.getPose().getY()**2+(line.x1()-self.getPose().getX())**2-self._radius**2

            delta = B**2-4*A*C
            if delta>=0:
                max_y = line.y2() if line.y2() > line.y1() else line.y1()
                min_y = line.y2() if line.y2() < line.y1() else line.y1()

                y1 = (-B-delta**0.5)/(2*A)
                y2 = (-B+delta**0.5)/(2*A)
                if y1 >= min_y and y1 <= max_y:
                    intersections.append(QPointF(line.x1(),y1))
                if y2 >= min_y and y2 <= max_y:  # appartient au segment
                    intersections.append(QPointF(line.x1(),y2))
        return intersections

