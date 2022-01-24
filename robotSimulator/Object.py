from PyQt5.QtGui import QPainter
from robotSimulator.representation.shapes import Point

class Object:

    def __init__(self,x,y,orientation,representation):
        self._pos = Point(x,y)
        self._orientation = orientation
        self._representation=representation
        self._representation.setParameters(self._pos,self._orientation)

    def getRepresentation(self):
        return self._representation

    def paint(self,window):
        painter=QPainter(window)
        self._representation.paint(painter)