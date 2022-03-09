from PyQt5.QtCore import QPoint

from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Point, Circle
from robotSimulator.sensors import Sensor


class ColorSensor(Sensor):

    BACKGROUND_COLOR = "#f0f0f0"

    def __init__(self,color="#000"):
        self._color = color
        self._representation = Representation(Circle(1,"#000"))
        super().__init__(self._representation)
        self._colorDetected = None

    def refresh(self):
        self._colorDetected=None
        if self._parent is not None:
            virtualObjects = sorted(self._parent.getEnv().getVirtualObjects(),key=lambda obj:obj.getZIndex())
            for obj in virtualObjects:
                if obj.getZIndex()<=self._parent.getZIndex():
                    if obj.getRepresentation().contains(self.getSensorPose()):
                        self._colorDetected = obj.getRepresentation().getShape().getColor().name()
            if self._colorDetected is None:
                self._colorDetected = self.BACKGROUND_COLOR

    def getSensorPose(self): # TODO : Méthode générale pour tous les capteurs et actionneurs !
        robotX = self._parent.getPose().getX()
        robotY = self._parent.getPose().getY()
        dx = self._pose.getX()
        dy = self._pose.getY()
        colorSensorX, colorSensorY = Point.computeTransformation(robotX, robotY, dx, dy,self._parent.getPose().getOrientation())
        colorSensorPose = QPoint(colorSensorX, colorSensorY)
        return colorSensorPose

    def getValue(self):
        return self._colorDetected

    def getSpecifications(self):
        specifications = "Current detected color : " + self._colorDetected
        return specifications










