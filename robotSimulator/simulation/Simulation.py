import sys
from PyQt5.QtWidgets import QApplication, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt
from robotSimulator import Interface
from robotSimulator.interface.ToolsBar import ToolsBar
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
        self._acceleration = 1
        self._timeElapsed = 0

    def run(self):
        th = threading.Thread(target=self.__run)
        th.start()

    def __run(self):
        start = time.time()
        while True:
            current=time.time()
            if current-start > config["time_step"]/self._acceleration:
                start = current
                self._timeElapsed+=config["time_step"]*self._acceleration

                for obj in self._environment.getObjects():
                    if hasattr(obj,"move"):
                        obj.move()
                    if hasattr(obj,"refresh"):
                        obj.refresh()
            time.sleep(self.MINIMUM_TIME_STEP)

    def showInterface(self):
        if self._environment is not None and not self._shown:
            th=threading.Thread(target=self.__startApplication)
            th.start()
            self._shown = True

    def __startApplication(self):
        app = QApplication([sys.argv])
        myInterface = Interface(self._environment)
        sys.exit(app.exec())

    def setAcceleration(self,acc):
        self._acceleration=acc

    def time(self):
        return self._timeElapsed

    def getAcceleration(self):
        return self._acceleration

    def getTimeElapsed(self):
        return self._timeElapsed



