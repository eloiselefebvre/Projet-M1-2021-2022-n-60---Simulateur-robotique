from robotSimulator.representation.shapes import Point

class Pose:

    def __init__(self, x, y,orientation=0,rx=0,ry=0):
        self._pose = Point(x,y)
        self.setRot(rx,ry)
        self._orientation = orientation

    def getX(self):
        return self._pose.getX()

    def getY(self):
        return self._pose.getY()

    def getRotX(self):
        return self._rotationCenter.getX()

    def getRotY(self):
        return self._rotationCenter.getY()

    def getOrientation(self):
        return self._orientation

    def setRot(self,rx,ry):
        self._rotationCenter=Point(rx,ry)

    def rotate(self, angle):
        self._orientation += angle

    def move(self,x,y):
        self._pose.move(x,y)