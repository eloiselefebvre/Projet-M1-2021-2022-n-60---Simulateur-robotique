from . import Telemeter
from ..Object import Object
from ..Pose import Pose
from ..representation import Representation
from ..representation.shapes import Circle, Point
from ..config import config

class LIDAR(Telemeter):

    ANGULAR_RESOLUTION = 6
    SCAN_RATE = 300 # rpm

    # TODO : Revoir le fonctionnement du LIDAR dans l'environnement

    def __init__(self, color="#f00"):
        super().__init__(color)
        self._representation.setShape(Circle(6,"#1C1E32"))
        rep=Representation(Circle(2,self._color))
        rep.setPose(Pose(0,0))
        self._representation.addSubRepresentation(rep)
        self._angularSteps=int(360/self.ANGULAR_RESOLUTION)
        self._intersectionsBuffer = [None for _ in range(self._angularSteps)]
        self._bufferIndex=0
        self._laser.getRepresentation().setVisible(False)


    def refresh(self):
        for i in range(self._angularSteps):
            if self._parent is not None and self._intersectionsBuffer[i] is not None:
                self._parent.getEnv().removeObject(self._intersectionsBuffer[i])
            intersection = self.getClosestCollisitionPointAndComputeDistance()
            if self._parent is not None and intersection is not None:
                point = Object(Representation(Point(int(intersection.x()), int(intersection.y()), self._color)))
                point.setVisible(self.isVisible() and (self._parent.isVisible() if self._parent is not None else True))
                self._intersectionsBuffer[i]=point
                # self._parent.getEnv().addVirtualObject(point)
            self.getPose().rotate(self.ANGULAR_RESOLUTION)
        self._bufferIndex=(self._bufferIndex+1)%self._angularSteps