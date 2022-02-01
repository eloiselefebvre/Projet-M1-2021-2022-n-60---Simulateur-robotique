from robotSimulator import Object, Pose
from robotSimulator.sensors.Sensor import Sensor
from robotSimulator.representation.Representation import Representation
from robotSimulator.representation.shapes.Rectangle import Rectangle
from robotSimulator.representation.shapes.Line import Line


class Telemeter(Sensor):

    def __init__(self,color="#f00"):
        self._representation = Representation(Rectangle(16,8,color))
        super().__init__(self._representation)
        laserRep = Representation(Line(1000,2,color))
        laser = Object(laserRep)
        laser.setPose(Pose(0,0))
        self._representation.addSubRepresentation(laser.getRepresentation())

    # MSO TODO (Objectif) : Implémenter ceci en calculant l'intersection avec les autres formes de l'environnement
    def getValue(self):
        pass