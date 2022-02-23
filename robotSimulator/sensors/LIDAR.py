from . import Telemeter
from .. import Object, Pose
from ..representation import Representation
from ..representation.shapes import Circle, Point

class LIDAR(Telemeter):

    ROTATION_STEP = 5

    def __init__(self, color="#f00"):
        super().__init__(color)
        self._representation.setShape(Circle(6,"#1C1E32"))
        rep=Representation(Circle(2,self._color))
        rep.setPose(Pose(0,0))
        self._representation.addSubRepresentation(rep)
        self._intersections_buffer = [None for _ in range(int(360/self.ROTATION_STEP))]
        self._laser.getRepresentation().setVisible(False)


    def refresh(self):
        for i in range(int(360/self.ROTATION_STEP)):
            if self._parent is not None and self._intersections_buffer[i] is not None:
                self._parent.getEnv().removeObject(self._intersections_buffer[i])
            intersection = self.getClosestCollisitionPointAndComputeDistance()
            self._laserLine.setLength(3)
            if self._parent is not None and intersection is not None:
                point = Object(Representation(Point(int(intersection.x()), int(intersection.y()), self._color)))
                point.setSolid(False)
                self._intersections_buffer[i]=point
                self._parent.getEnv().addObject(point)
            self.getPose().rotate(self.ROTATION_STEP)
