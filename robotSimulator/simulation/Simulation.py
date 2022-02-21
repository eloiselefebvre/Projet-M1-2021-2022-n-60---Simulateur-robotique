import sys
from PyQt5.QtWidgets import QApplication, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt
from robotSimulator import Interface
from robotSimulator.simulation import Environment
import threading
import time

from robotSimulator.config import *


class Simulation():

    # MSO TODO : ajouter un paramètre pour le pas de temps + un membre dans la classe
    # (servira aussi plus tard pour l'interface graphique : un slider permettra de modifier ce membre)

    MINIMUM_TIME_STEP = 0.01

    def __init__(self,environment=None,timeStep=MINIMUM_TIME_STEP):
        self._environment=environment
        self._shown = False
        self._timeStep = timeStep

    def run(self):
        th = threading.Thread(target=self.__run)
        th.start()

    def __run(self):
        start = time.time()
        while True:
            current=time.time()
            if current-start > config["time_step"]:
                start = current
                for obj in self._environment.getObjects():
                    if hasattr(obj,"move"):
                        obj.move()
            time.sleep(self._timeStep)

    def showInterface(self):
        if self._environment is not None and not self._shown:
            th=threading.Thread(target=self.__startApplication)
            th.start()
            self._shown = True

    def __startApplication(self):
        app = QApplication([sys.argv])
        myInterface = Interface(self._environment)
        sys.exit(app.exec())

    def setTimeStep(self,timeStep):
        self._timeStep=timeStep
        #timeStepSlider = QSlider(Qt.Horizontal)
        #timeStepSlider.setTickPosition(QSlider.TickPosition)
        #timeStepSlider.setTickInterval(50)
        #timeStepSlider.setSingleStep(1)
        #return timeStepSlider.value()






