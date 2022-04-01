from discoverySimulator.Pose import Pose
from discoverySimulator.representation.shapes import Point

class Frame:

    """ The Frame class provides a Frame."""

    def __init__(self,coordinates=None,baseFrame=None):
        self.__coordinates=None
        self.__baseFrame=None
        self.setCoordinates(coordinates)
        self.setBaseFrame(baseFrame)

    # SETTERS
    def setCoordinates(self,coordinates):
        if isinstance(coordinates,Pose):
            self.__coordinates=coordinates

    def setBaseFrame(self,baseFrame):
        if isinstance(baseFrame,Frame):
            self.__baseFrame = baseFrame

    # GETTERS
    def getBaseFrame(self):
        return self.__baseFrame

    def getCoordinates(self):
        return self.__coordinates

    def getAbsoluteCoordinates(self):
        if self.__baseFrame is not None:
            absBf = self.__baseFrame.getAbsoluteCoordinates()
            bfX = absBf.getX()
            bfY = absBf.getY()

            dx = self.__coordinates.getX()
            dy = self.__coordinates.getY()

            X, Y = Point.computeTransformation(bfX, bfY, dx, dy, absBf.getOrientation())

            abs=Pose(X,Y,absBf.getOrientation()+self.__coordinates.getOrientation())
            del absBf
            return abs
        else:
            return self.__coordinates.copy()