from . import Telemeter
from ..Object import Object
from ..Pose import Pose
from ..representation import Representation
from ..representation.shapes import Circle, Point
from ..config import config


class LIDAR(Telemeter):
    ANGULAR_RESOLUTION = 6
    ANGULAR_RANGE = 360
    SCAN_RATE = 300  # rpm

    # TODO : Revoir le fonctionnement du LIDAR dans l'environnement

    def __init__(self, color="#f00"):
        super().__init__(color)
        self._representation.setShape(Circle(6, "#1C1E32"))
        rep = Representation(Circle(2, self._color))
        rep.setPose(Pose(0, 0))
        self._representation.addSubRepresentation(rep)
        self._angularSteps = int(self.ANGULAR_RANGE / self.ANGULAR_RESOLUTION)
        self._intersectionsBuffer = [None for _ in range(self._angularSteps)]
        self._bufferIndex = 0
        self._laser.getRepresentation().setVisible(False)

        self._ddegree = 0

    def refresh(self):
        step = self.SCAN_RATE * 360 * config["sensor_time_step"] / 60
        self._ddegree += step
        if self._ddegree > self.ANGULAR_RESOLUTION:
            self._ddegree -= self.ANGULAR_RESOLUTION
            if self.getPose().getOrientation() < self.ANGULAR_RANGE / 2 or self.getPose().getOrientation() > 360 - self.ANGULAR_RANGE / 2:
                if self._parent is not None and self._intersectionsBuffer[self._bufferIndex] is not None:
                    self._parent.getEnv().removeVirtualObject(self._intersectionsBuffer[self._bufferIndex])

                intersection = self.getClosestCollisitionPointAndComputeDistance()
                if self._parent is not None and intersection is not None:
                    point = Object(Representation(Point(int(intersection.x()), int(intersection.y()), self._color)))
                    point.setVisible(
                        self.isVisible() and (self._parent.isVisible() if self._parent is not None else True))
                    self._intersectionsBuffer[self._bufferIndex] = point
                    point.setZIndex(2)
                    self._parent.getEnv().addVirtualObject(point)

                self._bufferIndex = (self._bufferIndex + 1) % self._angularSteps
            self.getPose().rotate(step)
