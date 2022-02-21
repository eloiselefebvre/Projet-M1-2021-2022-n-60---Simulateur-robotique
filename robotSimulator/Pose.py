from robotSimulator import Point


class Pose(Point):

    def __init__(self, x, y,orientation=0,rx=0,ry=0):
        super().__init__(x, y)
        self._rx = rx
        self._ry = ry
        self._orientation = orientation

    def getRotX(self):
        return self._rx

    def getRotY(self):
        return self._ry

    def getOrientation(self):
        return self._orientation

    def setRot(self,rx,ry):
        self._rx=rx
        self._ry=ry

    def rotate(self, angle):
        self._orientation += angle

    def __add__(self, other):
        if isinstance(other,Pose):
            return Pose(self._x+other.getX(),self._y+other.getY(),self._orientation+other.getOrientation(),self._rx+other.getRotX(),self._ry+other.getRotY())

    def __str__(self):
        return super().__str__() + ", " + str(self._orientation)
