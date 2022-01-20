from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from . import Shape

class Circle(Shape):

    def __init__(self,radius,color,opacity=255):
        super().__init__(color,opacity)
        self._radius=radius

    def paint(self,painter,origin,orientation):
        super().paint(painter, origin, orientation)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawEllipse(-self._radius,-self._radius,self._radius*2,self._radius*2) # dessiné à partir du center