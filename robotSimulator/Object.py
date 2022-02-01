from PyQt5.QtGui import QPainter
from robotSimulator.representation.shapes import Point

class Object:

    def __init__(self,representation):
        self._origin = Point(0, 0)
        self._orientation = 0
        self._representation=representation

    def getRepresentation(self):
        return self._representation

    def paint(self,window):
        painter=QPainter(window)
        self._representation.paint(painter)

    def setParameters(self,origin,orientation):
        self._origin = origin
        self._orientation=orientation
        self._representation.setParameters(self._origin,self._orientation)

    def getOrigin(self):
        return self._origin