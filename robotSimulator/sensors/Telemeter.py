from robotSimulator.sensors.Sensor import Sensor
from robotSimulator.Representation import Representation
from robotSimulator.Rectangle import Rectangle
from robotSimulator.Line import Line
from robotSimulator.Point import Point

class Telemeter(Sensor):

    def __init__(self,x,y,orientation):
        self._representation = Representation(Rectangle(16,8,"#f00"))
        super().__init__(x, y, orientation, self._representation)
        laserShape = Line(1000,2,"#f00")
        laser = Representation(laserShape)
        self._representation.addSubRepresentation(laser)

    def getValue(self):
        pass