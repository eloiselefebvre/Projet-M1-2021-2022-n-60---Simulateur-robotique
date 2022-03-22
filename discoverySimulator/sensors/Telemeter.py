from discoverySimulator.Object import Object
from discoverySimulator.Pose import Pose
from discoverySimulator.representation.shapes.Point import Point
from discoverySimulator.sensors import Sensor
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes import Rectangle, Line

class Telemeter(Sensor):

    INFINITE_LENGTH = 10000 # TODO : add telemeter mesuring range

    def __init__(self,color:str="#f00"):
        """
        This method is used to create a new telemeter
        :param color: color of the telemeter
        """
        self._color = color
        self._representation = Representation(Rectangle(16,8,self._color))
        super().__init__(self._representation)
        self.__laserLine = Line(Telemeter.INFINITE_LENGTH, 2, self._color)
        laserRep = Representation(self.__laserLine)
        self._laser = Object(laserRep)
        self._laser.setPose(Pose(0,0))
        self._representation.addSubRepresentation(self._laser.getRepresentation())
        self._distance = Telemeter.INFINITE_LENGTH

    def getValue(self) -> float:
        """
        This method allows to get the value of the telemeter
        :return: value of the telemeter
        """
        return self._distance

    def getSpecifications(self) -> str:
        specifications=f"Current measured distance : {round(self._distance,1)}px<br>---<br>"
        specifications+=f"Measurement Range : ?px-?px"
        return specifications

    def getClosestCollisitionPointAndComputeDistance(self):
        intersections = []
        self.__laserLine.setLength(Telemeter.INFINITE_LENGTH)
        self._distance = self.INFINITE_LENGTH
        telemeterPose=self._frame.getAbsoluteCoordinates()
        self._laser.setPose(telemeterPose)
        for obj in self._env.getObjects():
            if obj != self._parent and obj!=self:
                intersections.extend(self._laser.getIntersectionsWith(obj))
        closest_point = None
        for point in intersections:
            di = ((self._laser.getPose().getX() - point.x()) ** 2 + (self._laser.getPose().getY() - point.y()) ** 2) ** 0.5
            if di < self._distance:
                self._distance = di
                closest_point = point
        self._laser.setPose(Pose(0, 0))
        return closest_point

    def refresh(self):
        self._laser.setVisible(False)
        previousDistance=self._distance
        self.getClosestCollisitionPointAndComputeDistance()
        if self._distance!=previousDistance:
            self.notifyObservers("stateChanged")
        self._laser.setVisible(True)
        self.__laserLine.setLength(int(self._distance))

