from PyQt5.QtGui import QPainter


class Object:

    def __init__(self,xPos,yPos,orientation,representation):
        self._xPos = xPos
        self._yPos = yPos
        self._orientation = orientation
        self._representation=representation
        self._representation.setParameters(self._xPos,self._yPos,self._orientation)

    def getRepresentation(self):
        return self._representation

    def paint(self,window):
        painter=QPainter(window)
        self._representation.paint(painter)