from robotSimulator.sensors.Sensor import Sensor
from robotSimulator.Representation import Representation
from robotSimulator.Rectangle import Rectangle
from robotSimulator.Point import Point

class Telemeter(Sensor):

    def __init__(self,x,y,orientation):
        self._representation = Representation(Rectangle(16,8,"#f00"))
        super().__init__(x, y, orientation, self._representation)
        laserShape = Rectangle(2,100,"#00f")
        laserShape.removeOrientationMark()
        laser = Representation(laserShape)
        laser.setParameters(Point(0,54),0)
        self._representation.addSubRepresentation(laser)

    def getValue(self):
        pass