class Pose:

    def __init__(self, x:float, y:float,orientation:float=0,rx:float=0,ry:float=0):
        """
        This method is used to create a pose for an object
        :param x: x coordinate in the environment
        :param y: y coordinate in the environment
        :param orientation: orientation in the environment
        :param rx: the rotation center x coordinate in the environment
        :param ry:  the rotation center y coordinate in the environment
        """
        self._pose = [x,y]
        self.setRotationCenter(rx, ry)
        self._orientation = orientation

    # SETTERS
    def setX(self,x:float):
        """
        This method is used to set the x coordinate of an object in the environment
        :param x: new x coordinate
        """
        self._pose[0]=x

    def setY(self,y:float):
        """
        This method is used to set the y coordinate of an object in the environment
        :param y: new y coordinate
        """
        self._pose[1]=y

    def setOrientation(self, orientation:float):
        """
        This method is used to set the orientation of an object in the environment
        :param orientation: new orientation
        """
        self._orientation=orientation

    def setRotationCenter(self, rx:float, ry:float):
        """
        This method is used to set the x rotation center coordinate of an object in the environment
        :param rx: new x rotation center coordinate
        """
        self._rotationCenter=(rx,ry)

    # GETTERS
    def getX(self) -> float:
        """
        This method is used to get the x coordinate of an object in the environment
        :return : the x coordinate of the environment
        """
        return self._pose[0]

    def getY(self) -> float:
        """
        This method is used to get the y coordinate of an object in the environment
        :return : the y coordinate of the environment
        """
        return self._pose[1]

    def getRotationCenterX(self) -> float:
        """
        This method is used to get the x rotation center coordinate of an object in the environment
        :return : the x rotation center coordinate of the environment
        """
        return self._rotationCenter[0]

    def getRotationCenterY(self) -> float:
        """
        This method is used to get the y rotation center coordinate of an object in the environment
        :return : the y rotation center coordinate of the environment
        """
        return self._rotationCenter[1]

    def getOrientation(self) -> float:
        """
        This method is used to get the orientation of an object in the environment
        :return : the orientation of the environment
        """
        return self._orientation

    def move(self,x:float,y:float):
        self._pose=[x,y]

    def rotate(self, angle:float):
        self._orientation = (self._orientation+angle)%360

    def copy(self):
        return Pose(self._pose[0],self._pose[1],self._orientation,self._rotationCenter[0],self._rotationCenter[1])