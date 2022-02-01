from robotSimulator import Point


class Pose(Point):

    def __init__(self, x, y, orientation=0):
        super().__init__(x, y)
        self._orientation = orientation

    def getOrientation(self):
        return self._orientation

    def rotate(self, angle):
        self._orientation += angle

    def __str__(self):
        return super().__str__() + ", " + str(self._orientation)
