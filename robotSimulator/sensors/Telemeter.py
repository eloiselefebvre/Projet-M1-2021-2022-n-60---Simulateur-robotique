from robotSimulator.sensors.Sensor import Sensor
from robotSimulator.representation.Representation import Representation
from robotSimulator.representation.shapes.Rectangle import Rectangle
from robotSimulator.representation.shapes.Line import Line


class Telemeter(Sensor):

    def __init__(self): # MSO TODO : Ajouter une couleur en paramètre, qui aurait une valeur par défaut
        self._representation = Representation(Rectangle(16,8,"#f00"))       # MSO TODO : si #f00 est la couleur par défaut du télémètre, mettre un membre pour ça, que vous pourrez rétutiliser pour le laser
        super().__init__(self._representation)
        laserShape = Line(1000,2,"#f00")        # MSO : TODO : Retirer ce 1000 en dur
        laser = Representation(laserShape)
        self._representation.addSubRepresentation(laser)

    # MSO TODO (Objectif) : Implémenter ceci en calculant l'intersection avec les autres formes de l'environnement
    def getValue(self):
        pass