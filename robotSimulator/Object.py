from PyQt5.QtGui import QPainter

class Object:

    def __init__(self,representation):
        self._pose = None
        self._representation = representation
        self._env= None

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

    def setEnv(self,env):
        self._env=env
