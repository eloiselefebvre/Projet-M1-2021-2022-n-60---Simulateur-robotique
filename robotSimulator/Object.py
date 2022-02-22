from PyQt5.QtGui import QPainter


class Object:

    def __init__(self,representation):
        self._pose = None
        self._representation = representation
        self._env= None
        self._collided = False

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

    def getEnv(self):
        return self._env

    def getCollidedState(self):
        return self._collided

    def setCollidedState(self,state):
        self._collided=state

    def isCollided(self):
        if not self._collided:
            for obj in self._env.getObjects():
                if self!=obj:
                    if self.isCollidedWith(obj):
                        self._collided=True
                        obj.setCollidedState(True)

    def isCollidedWith(self,obj):
        return self.getRepresentation().getShape().isCollidedWith(obj.getRepresentation().getShape())


