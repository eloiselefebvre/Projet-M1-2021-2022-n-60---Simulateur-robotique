import sys
from PyQt5.QtWidgets import QApplication
from robotSimulator import Interface
import threading
from robotSimulator.robots import Robot
import time

from robotSimulator.config import *



class Simulation:

    # MSO TODO : ajouter un paramètre pour le pas de temps + un membre dans la classe
    # (servira aussi plus tard pour l'interface graphique : un slider permettra de modifier ce membre)

    MINIMUM_TIME_STEP = 0.01

    def __init__(self,environment=None):
        self._environment=environment
        self._shown = False

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
                    if isinstance(obj,Robot):
                        obj.move()
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

