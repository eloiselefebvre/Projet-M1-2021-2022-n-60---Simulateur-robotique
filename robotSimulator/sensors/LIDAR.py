from . import Telemeter
from ..Object import Object
from ..Pose import Pose
from ..representation import Representation
from ..representation.shapes import Circle, Point
from ..config import config


class LIDAR(Telemeter):
    ANGULAR_RESOLUTION = 6 # degrees
    ANGULAR_RANGE = 360 # degrees
    SCAN_RATE = 300  # rpm
    # TODO : Rendre modifiable par l'utilisateur mais avec valeurs par défaut

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

        self._step_per_second = self.SCAN_RATE/60 * 360 / self.ANGULAR_RESOLUTION

    def refresh(self):
        steps_number = int(self._step_per_second * config["update_time_step"]/(self._acceleration if self._parent is None else self._parent.getAcceleration()))
        for _ in range(steps_number):
            if self.getPose().getOrientation() < self.ANGULAR_RANGE / 2 or self.getPose().getOrientation() > 360 - self.ANGULAR_RANGE / 2:
                if self._intersectionsBuffer[self._bufferIndex] is not None:
                    self._env.removeVirtualObject(self._intersectionsBuffer[self._bufferIndex])

                intersection = self.getClosestCollisitionPointAndComputeDistance()
                if intersection is not None:
                    point = Object(Representation(Point(int(intersection.x()), int(intersection.y()), self._color)))
                    point.setVisible(self.isVisible() and (self._parent.isVisible() if self._parent is not None else True))
                    self._intersectionsBuffer[self._bufferIndex] = point
                    point.setZIndex(2)
                    self._env.addVirtualObject(point)

                self._bufferIndex = (self._bufferIndex + 1) % self._angularSteps
            self.getPose().rotate(self.ANGULAR_RESOLUTION)

    def getSpecifications(self):
        specifications = "---\n"
        specifications += f"Angular Resolution : {self.ANGULAR_RESOLUTION}°\n"
        specifications += f"Angular Range : {self.ANGULAR_RANGE}°\n"
        specifications += f"Scan Rate : {self.SCAN_RATE}rpm"
        return specifications
