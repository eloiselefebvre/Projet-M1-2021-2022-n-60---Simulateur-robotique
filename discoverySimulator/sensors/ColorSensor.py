from PyQt5.QtCore import QPoint

from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle
from discoverySimulator.sensors import Sensor

class ColorSensor(Sensor):

    def __init__(self,color:str=None):
        """
        This method is used to create a new color sensor
        :param color: color of the sensor
        """
        self._color = color
        self._representation = Representation(Circle(1,"#000"))
        super().__init__(self._representation)
        self._colorDetected = None

    # GETTERS
    def getValue(self) -> str:
        """
        This method allows to get the captured color by the sensor
        :return: the captured color
        """
        return self._colorDetected

    def getSpecifications(self):
        """
        This method is used to get specifications about the color sensor
        :return: specifications about the color sensor
        """
        return "Current detected color : " + self._colorDetected

    def refresh(self):
        previousColor=self._colorDetected
        self._colorDetected=None
        sensorPose = self._frame.getAbsoluteCoordinates()
        colorSensorPoint = QPoint(round(sensorPose.getX()),round(sensorPose.getY()))
        virtualObjects = sorted(self._environnement.getVirtualObjects(), key=lambda obj:obj.getZIndex())
        for obj in virtualObjects:
            if obj.getZIndex()<=self._parent.getZIndex():
                if obj.getRepresentation().contains(colorSensorPoint):
                    self._colorDetected = obj.getRepresentation().getShape().getColor()
        if self._colorDetected is None:
            self._colorDetected = colors['sceneBackground']
        if self._colorDetected!=previousColor:
            self.notifyObservers("stateChanged")












