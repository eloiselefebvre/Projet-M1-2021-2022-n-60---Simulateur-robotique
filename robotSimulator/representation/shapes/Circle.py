from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QColor
from . import Shape

class Circle(Shape):

    def __init__(self,radius,color,opacity=255):
        super().__init__(color,opacity)
        self._radius=radius
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None

        self._x1i = None
        self._x2i = None
        self._y1i = None
        self._y2i = None

    def getRadius(self):
        return self._radius

    def paint(self,painter):
        if self._x1 is not None:
            painter.setPen(QPen(QColor("#f00"), 2, Qt.SolidLine))
            #painter.drawLine(self._x1,self._y1,self._x2,self._y2)
            painter.setPen(QPen(QColor("#f0f"), 4, Qt.SolidLine))
            painter.drawPoint(self._x1i,self._y1i)
            painter.drawPoint(self._x2i,self._y2i)
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawEllipse(-self._radius,-self._radius,self._radius*2,self._radius*2) # dessiné à partir du center

    def isIntersectionWithLine(self,line):

        if line.x2()!=line.x1(): # pas ligne verticale
            a_line=(line.y2()-line.y1())/(line.x2()-line.x1())
            b_line=line.y1()-a_line*line.x1()

            A = 1+a_line**2
            B = -2*self._pose.getX()+2*a_line*(b_line-self._pose.getY())
            C = self._pose.getX()**2 + (b_line-self._pose.getY())**2 - self._radius**2

            delta = B**2-4*A*C

            if delta < 0:
                return False
            else:
                max_x = line.x2() if line.x2() > line.x1() else line.x1()
                min_x = line.x2() if line.x2() < line.x1() else line.x1()
                self._x1 = int(min_x - 20)
                self._x2 = int(max_x + 20)
                self._y1 = int(a_line * self._x1 + b_line)
                self._y2 = int(a_line * self._x2 + b_line)

                self._x1i  = int((-B - delta ** 0.5) / (2 * A))
                self._x2i = int((-B + delta ** 0.5) / (2 * A))
                self._y1i = int((a_line * self._x1i) + b_line)
                self._y2i = int((a_line * self._x2i) + b_line)

                if (self._x1i >= min_x and self._x1i <= max_x) or (self._x2i >= min_x and self._x2i <= max_x):  # appartient au segment
                    return True
                return False

        if line.x2()==line.x1(): # ligne verticale
            A = 1
            B = -2*self._pose.getY()
            C = self._pose.getY()**2 + (line.x1()-self._pose.getX())**2 - self._radius**2

            delta = B**2-4*A*C

            if delta < 0:
                return False
            else:
                max_y = line.y2() if line.y2() > line.y1() else line.y1()
                min_y = line.y2() if line.y2() < line.y1() else line.y1()

            self._y1 = int(min_y - 20)
            self._y2 = int(max_y + 20)

            self._y1i = int((-B - delta ** 0.5) / (2 * A))
            self._y2i = int((-B + delta ** 0.5) / (2 * A))

            if (self._y1i >= min_y and self._y1i <= max_y) or (self._y2i >= min_y and self._y2i <= max_y):  # appartient au segment
                return True
            return False

        return False

