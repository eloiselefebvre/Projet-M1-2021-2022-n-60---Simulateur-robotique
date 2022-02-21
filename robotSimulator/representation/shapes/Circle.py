from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QColor
from . import Shape

class Circle(Shape):

    def __init__(self,radius,color,opacity=255):
        super().__init__(color,opacity)
        self._radius=radius
        self._x1=None
        self._y1 = None
        self._x2 = None
        self._y2 = None

        self._x1i = None
        self._x2i = None

    def getRadius(self):
        return self._radius

    def paint(self,painter):
        # if self._x1 is not None:
        #     painter.setPen(QPen(QColor("#f00"), 2, Qt.SolidLine))
        #     painter.drawLine(self._x1,self._y1,self._x2,self._y2)
        #     painter.setPen(QPen(QColor("#f0f"), 4, Qt.SolidLine))
            # painter.drawPoint(self._x1i,100)
            # painter.drawPoint(self._x2i, 120)
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawEllipse(-self._radius,-self._radius,self._radius*2,self._radius*2) # dessiné à partir du center

    def isIntersectionWithLine(self,line):
        if line.x2()!=line.x1() and line.y2()!=line.y1(): # pas ligne verticale ou horizontale
            a=(line.y2()-line.y1())/(line.x2()-line.x1())
            b=line.y2()-a*line.x2()

            max_x = line.x2() if line.x2() > line.x1() else line.x1()
            min_x = line.x2() if line.x2() < line.x1() else line.x1()
            self._x1 = int(min_x - 20)
            self._x2 = int(max_x + 20)
            self._y1 = int(a * (min_x - 20) + b)
            self._y2 = int(a * (max_x + 20) + b)

            A = 1+a**2
            B = -2*self._pose.getX()+2*a*(b-self._pose.getY())
            C = self._pose.getX()**2 + (b-self._pose.getY())**2 - self._radius**2

            #print(f"Delta = {B**2-4*A*C}")

            delta = B**2-4*A*C

            if delta<0:
                return False
            else:

                x1=(-b-delta**0.5)/(2*a)
                x2=(-b+delta**0.5)/(2*a)
                # print(f"a={a},b={b},delta={delta},x1={x1}, x2={x2}")


                self._x1i = int(x1)
                self._x2i = int(x2)
                if (x1>=min_x and x1<=max_x) or (x2>=min_x and x2<=max_x): # appartient au segment
                    # print("ok")
                    return True
                return False
        return False