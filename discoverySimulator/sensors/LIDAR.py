from . import Telemeter
from ..Object import Object
from ..Pose import Pose
from ..representation import Representation
from ..representation.shapes import Circle, Point
from ..config import config


class LIDAR(Telemeter):

    def __init__(self,color="#f00", scanRate=300, angularRange=360,angularResolution=6):
        """
        This method is used to create a LIDAR
        :param color: color of the LIDAR
        :param scanRate: scna rate of the LIDAR [rpm]
        :param angularRange: angular range of the LIDAR [degrees]
        :param angularResolution: angular resolution of the LIDAR [degrees]
        """
        super().__init__(color)
        self._representation.setShape(Circle(6, "#1C1E32"))
        rep = Representation(Circle(2, self._color))
        rep.setPose(Pose(0, 0))
        self._scanRate=scanRate
        self._angularRange=angularRange
        self._angularResolution=angularResolution
        self._representation.addSubRepresentation(rep)
        self._angularSteps = int(self._angularRange / self._angularResolution)
        self._intersectionsBuffer = [None for _ in range(self._angularSteps)]
        self._bufferIndex = 0
        self._laser.getRepresentation().setVisible(False)
        self._step_per_second = int(self._scanRate/60 * 360 / self._angularResolution)

    def refresh(self):
        steps_number = int(self._step_per_second * config["update_time_step"]*(self._acceleration if self._parent is None else self._parent.getAcceleration()))
        for _ in range(steps_number):
            if self.getPose().getOrientation() < self._angularRange / 2 or self.getPose().getOrientation() > 360 - self._angularRange / 2:
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
            self.getPose().rotate(self._angularResolution)

    def getSpecifications(self):
        specifications = "---<br>"
        specifications += f"Angular Resolution : {self._angularResolution}°<br>"
        specifications += f"Angular Range : {self._angularRange}°<br>"
        specifications += f"Scan Rate : {self._scanRate}rpm"
        return specifications
