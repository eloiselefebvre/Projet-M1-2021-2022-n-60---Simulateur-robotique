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

    MINIMUM_TIME_STEP = 0.01

    def __init__(self,environment=None):
        self._environment=environment
        self._app = None
        self._interface=None
        self._appShown = False
        self._acceleration = 1
        self._timeElapsed = 0
        self._play=True

    def run(self):
        th = threading.Thread(target=self.__run)
        th.start()

    def __run(self):
        start = time.time()
        while True:
            current=time.time()
            if current-start > config["time_step"]/self._acceleration and self._play:
                start = current
                self._timeElapsed+=config["time_step"]*self._acceleration
                for obj in self._environment.getObjects():
                    if hasattr(obj,"move"):
                        obj.move()
                    if hasattr(obj,"refresh"):
                        obj.refresh()
            time.sleep(self.MINIMUM_TIME_STEP)

    def showInterface(self):
        if self._environment is not None and not self._appShown:
            th=threading.Thread(target=self.__startApplication)
            th.start()
            self._appShown = True

    def __startApplication(self):
        self._app = QApplication([sys.argv])
        self._interface=Interface(self,self._environment)
        sys.exit(self._app.exec())

    def setAcceleration(self,acc):
        self._acceleration=acc

    def time(self):
        return self._timeElapsed

    def setAppShown(self,shown):
        self._appShown=shown

    def closeInterface(self):
        if self._appShown:
            self._appShown = False
            self._interface.close()
        # TODO : fermer également l'application ?

    def increaseAcceleration(self):
        pas=0.1
        self._acceleration+=pas

    def decreaseAcceleration(self):
        pas=0.1
        if self._acceleration-pas>0:
            self._acceleration-=pas

    def getAcceleration(self):
        return self._acceleration

    def playPause(self):
        self._play=not self._play

    def getPlay(self):
        return self._play

