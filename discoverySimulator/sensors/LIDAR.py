from . import Telemeter
from ..Object import Object
from ..Pose import Pose
from ..representation import Representation
from ..representation.shapes import Circle, Point
from ..config import config


class LIDAR(Telemeter):

    def __init__(self,color:str="#f00", scanRate:int=300, angularRange:int=360,angularResolution:int=6):
        """
        This method is used to create a LIDAR
        :param color: color of the LIDAR
        :param scanRate: scna rate of the LIDAR [rpm]
        :param angularRange: angular range of the LIDAR [degrees]
        :param angularResolution: angular resolution of the LIDAR [degrees]
        """
        super().__init__(color)
        self._laser.getRepresentation().setVisible(False)

        self._representation.setShape(Circle(6, "#1C1E32"))
        rep = Representation(Circle(2, self._color))
        rep.setPose(Pose(0, 0))
        self._representation.addSubRepresentation(rep)

        self.__scanRate=int(scanRate)
        self.__angularRange=int(angularRange)
        self.__angularResolution=int(angularResolution)
        self.__angularSteps = int(self.__angularRange / self.__angularResolution)
        self.__intersectionsBuffer = [None for _ in range(self.__angularSteps)]
        self.__bufferIndex = 0
        self.__stepPerSecond = int(self.__scanRate / 60 * 360 / self.__angularResolution)

    def refresh(self):
        steps_number = int(self.__stepPerSecond * config["update_time_step"] * (self._acceleration if self._parent is None else self._parent.getAcceleration()))
        for _ in range(steps_number):
            if self.getPose().getOrientation() < self.__angularRange / 2 or self.getPose().getOrientation() > 360 - self.__angularRange / 2:
                if self.__intersectionsBuffer[self.__bufferIndex] is not None:
                    self._environnement.removeVirtualObject(self.__intersectionsBuffer[self.__bufferIndex])

                intersection = self.getClosestCollisitionPointAndComputeDistance()
                if intersection is not None:
                    point = Object(Representation(Point(self._color)))
                    point.setVisible(self.isVisible() and (self._parent.isVisible() if self._parent is not None else True))
                    self.__intersectionsBuffer[self.__bufferIndex] = point
                    point.setZIndex(2)
                    self._environnement.addVirtualObject(point, intersection.x(), intersection.y())

                self.__bufferIndex = (self.__bufferIndex + 1) % self.__angularSteps
            self.getPose().rotate(self.__angularResolution)

    def getSpecifications(self) -> str:
        specifications = "---<br>"
        specifications += f"Angular Resolution : {self.__angularResolution}°<br>"
        specifications += f"Angular Range : {self.__angularRange}°<br>"
        specifications += f"Scan Rate : {self.__scanRate}rpm<br>"
        specifications += f"Measurement Range : 0px-{self._maximumMesurableDistance}px"
        return specifications
