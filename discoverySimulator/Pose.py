class Pose:

    """ The Pose class provides a pose"""

    def __init__(self, x:float, y:float,orientation:float=0,rx:float=0,ry:float=0):
        """ Constructs a pose for an object
        @param x  x coordinate in the environment
        @param y  y coordinate in the environment
        @param orientation  Orientation in the environment
        @param rx  The rotation center x coordinate in the environment
        @param ry  The rotation center y coordinate in the environment
        """
        self.__pose = [x, y]
        self.setRotationCenter(rx, ry)
        self.__orientation = orientation

    # SETTERS
    def setX(self,x:float):
        """ Sets the x coordinate of an object in the environment
        @param x  new x coordinate
        """
        self.__pose[0]=x

    def setY(self,y:float):
        """ Sets the y coordinate of an object in the environment
        @param y  New y coordinate
        """
        self.__pose[1]=y

    def setOrientation(self, orientation:float):
        """ Sets the orientation of an object in the environment
        @param orientation  New orientation
        """
        self.__orientation=orientation

    def setRotationCenter(self, rx:float, ry:float):
        """ Sets the x rotation center coordinate of an object in the environment
        @param rx  New x rotation center coordinate
        """
        self.__rotationCenter=(rx, ry)

    # GETTERS
    def getX(self) -> float:
        """ Returns the x coordinate of an object in the environment
        @return  The x coordinate of the environment
        """
        return self.__pose[0]

    def getY(self) -> float:
        """ Returns the y coordinate of an object in the environment
        @return  The y coordinate of the environment
        """
        return self.__pose[1]

    def getRotationCenterX(self) -> float:
        """ Returns the x rotation center coordinate of an object in the environment
        @return  The x rotation center coordinate of the environment
        """
        return self.__rotationCenter[0]

    def getRotationCenterY(self) -> float:
        """ Returns the y rotation center coordinate of an object in the environment
        @return  The y rotation center coordinate of the environment
        """
        return self.__rotationCenter[1]

    def getOrientation(self) -> float:
        """ Returns the orientation of an object in the environment
        @return  The orientation of the environment
        """
        return self.__orientation

    def move(self,x:float,y:float):
        self.__pose=[x, y]

    def rotate(self, angle:float):
        self.__orientation = (self.__orientation + angle) % 360

    def copy(self):
        return Pose(self.__pose[0], self.__pose[1], self.__orientation, self.__rotationCenter[0], self.__rotationCenter[1])