from math import radians, cos, sin

from robotSimulator import Object, Pose
from robotSimulator.sensors.Sensor import Sensor
from robotSimulator.representation.Representation import Representation
from robotSimulator.representation.shapes.Rectangle import Rectangle
from robotSimulator.representation.shapes.Line import Line

class Telemeter(Sensor):

    INFINITE_LENGTH = 10000

    def __init__(self,color="#f00"):
        self._representation = Representation(Rectangle(16,8,color))
        super().__init__(self._representation)
        self._laserLine = Line(self.INFINITE_LENGTH,2,color)
        laserRep = Representation(self._laserLine)
        self._laser = Object(laserRep)
        self._laser.setPose(Pose(0,0))
        self._representation.addSubRepresentation(self._laser.getRepresentation())
        self._distance = self.INFINITE_LENGTH

    def refresh(self):
        intersections = []
        # TODO : Telemeter dans l'environnement donc sans parent
        if self._parent is not None:
            robotX = self._parent.getPose().getX()
            robotY = self._parent.getPose().getY()

            dx = self._pose.getX()
            dy = self._pose.getY()
            a = -radians(self._parent.getPose().getOrientation())
            telemeterX = int(dx * cos(a) + dy * sin(a) + robotX)
            telemeterY = int(-dx * sin(a) + dy * cos(a) + robotY)
            self._laser.setPose(Pose(telemeterX,telemeterY,self._parent.getPose().getOrientation()+self._pose.getOrientation()))
            self._laserLine.setLength(self.INFINITE_LENGTH)
            for obj in self._parent.getEnv().getObjects():
                if obj != self._parent:
                    intersections.extend(self._laser.isCollidedWith(obj))

            self._distance=self.INFINITE_LENGTH
            for point in intersections:
                di=((self._laser.getPose().getX()-point.x())**2+(self._laser.getPose().getY()-point.y())**2)**0.5
                if di<self._distance :
                    self._distance=di
            self._laserLine.setLength(int(self._distance))
            self._laser.setPose(Pose(0, 0))

    def getValue(self):
        return self._distance
