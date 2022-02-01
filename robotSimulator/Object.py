from PyQt5.QtGui import QPainter
from robotSimulator import Point

class Object:

    def __init__(self, representation):
        #self._origin = Point(0,0)
        #self._orientation = 0
        self._pose = None
        self._representation = representation

    def getRepresentation(self):
        return self._representation

    def paint(self, window):
        painter = QPainter(window)
        self._representation.paint(painter)

    def setPose(self,pose):
        self._pose=pose
        self._representation.setPose(self._pose)

    def getPose(self):
        return self._pose
