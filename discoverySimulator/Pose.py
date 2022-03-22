class Pose:

    def __init__(self, x, y,orientation=0,rx=0,ry=0):
        self._pose = (x,y)
        self.setRotationCenter(rx, ry)
        self._orientation = orientation

    def getX(self):
        return self._pose[0]

    def getY(self):
        return self._pose[1]

    def getRotX(self):
        return self._rotationCenter[0]

    def getRotY(self):
        return self._rotationCenter[1]

    def getOrientation(self):
        return self._orientation

    def setOrientation(self,o):
        self._orientation=o

    def setRotationCenter(self, rx, ry):
        self._rotationCenter=(rx,ry)

    def rotate(self, angle):
        self._orientation = (self._orientation+angle)%360

    def move(self,x,y):
        self._pose=(x,y)

    def copy(self):
        return Pose(self._pose[0],self._pose[1],self._orientation)