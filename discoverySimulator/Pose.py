class Pose:

    def __init__(self, x:float, y:float,orientation:float=0,rx:float=0,ry:float=0):
        self._pose = [x,y]
        self.setRotationCenter(rx, ry)
        self._orientation = orientation

    def setX(self,x:float):
        self._pose[0]=x

    def setY(self,y:float):
        self._pose[1]=y

    def setOrientation(self, orientation:float):
        self._orientation=orientation

    def setRotationCenter(self, rx:float, ry:float):
        self._rotationCenter=(rx,ry)

    def getX(self) -> float:
        return self._pose[0]

    def getY(self) -> float:
        return self._pose[1]

    def getRotationCenterX(self) -> float:
        return self._rotationCenter[0]

    def getRotationCenterY(self) -> float:
        return self._rotationCenter[1]

    def getOrientation(self) -> float:
        return self._orientation

    def move(self,x:float,y:float):
        self._pose=[x,y]

    def rotate(self, angle:float):
        self._orientation = (self._orientation+angle)%360

    def copy(self):
        return Pose(self._pose[0],self._pose[1],self._orientation,self._rotationCenter[0],self._rotationCenter[1])