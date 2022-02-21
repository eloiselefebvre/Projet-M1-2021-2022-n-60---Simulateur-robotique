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
        laserRep = Representation(Line(self.INFINITE_LENGTH,2,color))
        self._laser = Object(laserRep)
        self._laser.setPose(Pose(0,0))
        self._representation.addSubRepresentation(self._laser.getRepresentation())

    # MSO TODO (Objectif) : Implémenter ceci en calculant l'intersection avec les autres formes de l'environnement
    def getValue(self):
        if self._parent is not None:
            self._laser.setPose(self.getPose()+self._parent.getPose())
            for obj in self._parent.getEnv().getObjects():
                if obj != self._parent:
                    if self._laser.isCollidedWith(obj): print(self._laser.isCollidedWith(obj))
            self._laser.setPose(Pose(0,0))