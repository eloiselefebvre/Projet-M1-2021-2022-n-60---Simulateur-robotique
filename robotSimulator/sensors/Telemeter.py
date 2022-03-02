from robotSimulator.Object import Object
from robotSimulator.Pose import Pose
from robotSimulator.representation.shapes.Point import Point
from robotSimulator.sensors import Sensor
from robotSimulator.representation.Representation import Representation
from robotSimulator.representation.shapes import Rectangle, Line

class Telemeter(Sensor):

    INFINITE_LENGTH = 10000

    def __init__(self,color="#f00"):
        self._color = color
        self._representation = Representation(Rectangle(16,8,self._color))
        super().__init__(self._representation)
        self._laserLine = Line(self.INFINITE_LENGTH,2,self._color)
        laserRep = Representation(self._laserLine)
        self._laser = Object(laserRep)
        self._laser.setPose(Pose(0,0))
        self._representation.addSubRepresentation(self._laser.getRepresentation())
        self._distance = self.INFINITE_LENGTH

    def getClosestCollisitionPointAndComputeDistance(self):
        intersections = []
        self._laserLine.setLength(self.INFINITE_LENGTH)
        self._distance = self.INFINITE_LENGTH
        if self._parent is not None:  # Telemeter monté sur un robot
            robotX = self._parent.getPose().getX()
            robotY = self._parent.getPose().getY()
            dx = self._pose.getX()
            dy = self._pose.getY()
            telemeterX, telemeterY = Point.computeTransformation(robotX, robotY, dx, dy,self._parent.getPose().getOrientation())
            self._laser.setPose(Pose(telemeterX, telemeterY, self._parent.getPose().getOrientation() + self._pose.getOrientation()))
            for obj in self._parent.getEnv().getObjects():
                if obj != self._parent:
                    intersections.extend(self._laser.isCollidedWith(obj))
        else:
            self._laser.setPose(self._pose)
            for obj in self._env.getObjects():
                if obj != self:
                    intersections.extend(self._laser.isCollidedWith(obj))
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
        self.getClosestCollisitionPointAndComputeDistance()
        self._laser.setVisible(True)
        self._laserLine.setLength(int(self._distance))

    def getValue(self):
        return self._distance
