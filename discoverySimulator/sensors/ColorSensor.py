from PyQt5.QtCore import QPoint
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle
from discoverySimulator.sensors import Sensor

class ColorSensor(Sensor):

    BACKGROUND_COLOR = "#f0f0f0"

    def __init__(self,color:str=None):
        """
        This method is used to create a new color sensor
        :param color: color of the sensor
        """
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
            self._colorDetected = ColorSensor.BACKGROUND_COLOR
        if self._colorDetected!=previousColor:
            self.notifyObservers("stateChanged")

    def getValue(self) -> str:
        """
        This method allows to get the captured color by the sensor
        :return: the captured color
        """
        return self._colorDetected

    def getSpecifications(self):
        return "Current detected color : " + self._colorDetected










