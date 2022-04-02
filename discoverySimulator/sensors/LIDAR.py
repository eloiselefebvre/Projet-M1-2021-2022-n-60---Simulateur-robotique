from . import Telemeter
from ..Object import Object
from ..Pose import Pose
from ..representation import Representation
from ..representation.shapes import Circle, Point
from ..config import config, colors


class LIDAR(Telemeter):

    """ The LIDAR class provides a LIDAR."""

    def __init__(self,color:str=colors['sensor'], scanRate:int=300, angularRange:int=360,angularResolution:int=7,maximumMeasurableDistance:int=None,accuracy:float=1):
        """ Constructs a LIDAR.
        @param color  Color of the LIDAR
        @param scanRate  Scan rate of the LIDAR [rpm]
        @param angularRange  Angular range of the LIDAR [degrees]
        @param angularResolution  Angular resolution of the LIDAR [degrees]"""
        super().__init__(color,maximumMeasurableDistance,accuracy)
        self._laser.getRepresentation().setVisible(False)

        self._representation.setShape(Circle(6, colors['LIDAR']))
        rep = Representation(Circle(2, self._color))
        rep.setPose(Pose(0, 0))
        self._representation.addSubRepresentation(rep)

        self.__scanRate=int(scanRate)
        self.__angularRange=int(angularRange)
        self.__angularResolution=int(angularResolution)
        self.__angularSteps = int(self.__angularRange / self.__angularResolution)
        self.__intersectionsBuffer = [None for _ in range(self.__angularSteps)]
        self.__distances=[None for _ in range(self.__angularSteps)]
        self.__bufferIndex = 0
        self.__stepPerSecond = int(self.__scanRate / 60 * 360 / self.__angularResolution)

    # GETTERS
    def getSpecifications(self) -> str:
        specifications = "<pre>"
        specifications += f"Angular Resolution : {self.__angularResolution}°<br>"
        specifications += f"Angular Range : {self.__angularRange}°<br>"
        specifications += f"Scan Rate : {self.__scanRate}rpm<br>"
        specifications += f"Measurement Range : 0px-{self._maximumMesurableDistance}px"
        if self._environment.isReal():
            specifications+=f"<br>Accuracy : ±{round(self._mesuringNoise*100,1)}%"
        specifications += "</pre>"
        return specifications

    def refresh(self):
        steps_number = round(self.__stepPerSecond * config["real_update_time_step"])
        for _ in range(steps_number):
            if self.getPose().getOrientation() < self.__angularRange / 2 or self.getPose().getOrientation() > 360 - self.__angularRange / 2:
                if self.__intersectionsBuffer[self.__bufferIndex] is not None:
                    self._environment.removeVirtualObject(self.__intersectionsBuffer[self.__bufferIndex])

                intersection = self.getClosestCollisitionPointAndComputeDistance()
                if intersection is not None:
                    point = Object(Representation(Point(self._color)))
                    point.setVisible(self.isVisible() and (self._parent.isVisible() if self._parent is not None else True))
                    self.__intersectionsBuffer[self.__bufferIndex] = point
                    point.setZIndex(2)
                    self._environment.addVirtualObject(point, intersection.x(), intersection.y())
                    self.__distances[self.__bufferIndex]=(self.getPose().getOrientation(),super().getValue())

                self.__bufferIndex =(self.__bufferIndex + 1) % self.__angularSteps
            self.getPose().rotate(self.__angularResolution)

    def getValue(self) -> list:
        return self.__distances


