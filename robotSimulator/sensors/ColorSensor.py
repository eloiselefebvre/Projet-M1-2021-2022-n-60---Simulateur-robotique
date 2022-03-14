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
        previousColor=self._colorDetected
        self._colorDetected=None

        sensorPose = self._frame.getAbsoluteCoordinates()
        colorSensorPoint = QPoint(sensorPose.getX(),sensorPose.getY())
        virtualObjects = sorted(self._env.getVirtualObjects(),key=lambda obj:obj.getZIndex())
        for obj in virtualObjects:
            if obj.getZIndex()<=self._parent.getZIndex():
                if obj.getRepresentation().contains(colorSensorPoint):
                    self._colorDetected = obj.getRepresentation().getShape().getColor().name()
        if self._colorDetected is None:
            self._colorDetected = self.BACKGROUND_COLOR
        if self._colorDetected!=previousColor:
            self.notifyObservers("stateChanged")

    def getValue(self):
        return self._colorDetected

    def getSpecifications(self):
        return "Current detected color : " + self._colorDetected










