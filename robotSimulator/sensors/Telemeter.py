from robotSimulator.sensors.Sensor import Sensor
from robotSimulator.representation.Representation import Representation
from robotSimulator.representation.shapes.Rectangle import Rectangle
from robotSimulator.representation.shapes.Line import Line


class Telemeter(Sensor):

    def __init__(self,x,y,orientation):
        self._representation = Representation(Rectangle(16,8,"#f00"))
        super().__init__(x, y, orientation, self._representation)
        laserShape = Line(1000,2,"#f00")
        laser = Representation(laserShape)
        self._representation.addSubRepresentation(laser)

    def getValue(self):
        pass