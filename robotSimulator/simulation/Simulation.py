import sys
from PyQt5.QtWidgets import QApplication
from robotSimulator.interface.views.Interface import Interface
from robotSimulator.Observable import Observable
import threading
import time
from robotSimulator.config import *

class Simulation(Observable):

    MINIMUM_TIME_STEP = 0.005

    def __init__(self,environment=None):
        super().__init__()
        self._environment=environment
        self._app = None
        self._interface=None
        self._appShown = False
        self._acceleration = 1
        self._timeElapsed = 0
        self._playState=True

    def run(self):
        th = threading.Thread(target=self.__run)
        th.start()

    def __run(self):
        start_robot = time.time()
        start_sensor = time.time()
        while True:
            current=time.time()
            if self._playState:
                if current-start_robot > config["time_step"]/self._acceleration:
                    start_robot = current
                    self._timeElapsed+=config["time_step"]*self._acceleration
                    for obj in self._environment.getObjects():
                        if hasattr(obj,"move"):
                            obj.move()
                    self.notifyObservers("poseChanged")
                if current-start_sensor > config["sensor_time_step"]/self._acceleration:
                    start_sensor = current
                    for sensor in self._environment.getSensors():
                        if hasattr(sensor, "refresh"):
                            sensor.refresh()
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

    def setAcceleration(self,acc): # TODO : Notify toolsbar
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

    def getAcceleration(self):
        return self._acceleration

    def updateAcceleration(self,sender):
        self._acceleration=sender.getAcceleration()

    def updatePlayState(self,sender):
        self._playState=sender.getPlayState()

