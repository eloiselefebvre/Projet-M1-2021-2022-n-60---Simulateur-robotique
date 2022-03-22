import sys
from PyQt5.QtWidgets import QApplication
from discoverySimulator.interface.views.Interface import Interface
from discoverySimulator.Observable import Observable
import threading
import time
from discoverySimulator.config import *

class Simulation(Observable):

    MINIMUM_TIME_STEP = 0.01

    def __init__(self,environment=None):
        """
        This method is used to create a new simulation
        :param environment: environment where the simulation will take place
        """
        super().__init__()
        self._environment=environment
        self._app = None
        self._interface=None
        self._appShown = False
        self._acceleration = 1
        self._timeElapsed = 0
        self._playState=True

    def run(self):
        """
        This method allows to run the simulation
        """
        th = threading.Thread(target=self.__run)
        th.start()

    def __run(self):
        start_update = time.time()
        while True:
            current=time.time()
            if current - start_update > config["update_time_step"] / self._acceleration:
                start_update = current

                # ROBOT UPDATE
                if self._playState:
                    self._timeElapsed += config["update_time_step"] * self._acceleration

                    self.notifyObservers("timeChanged")
                    for obj in self._environment.getObjects():
                        if hasattr(obj, "move"):
                            obj.move()

                # SENSOR UPDATE
                for sensor in self._environment.getSensors():
                    if hasattr(sensor, "refresh"):
                        sensor.refresh()
            time.sleep(self.MINIMUM_TIME_STEP)

    def showInterface(self):
        """
        This method allows to show the interface where the simulation takes place
        """
        if self._environment is not None and not self._appShown:
            th=threading.Thread(target=self.__startApplication)
            th.start()
            self._appShown = True

    def __startApplication(self):
        self._app = QApplication([sys.argv])
        self._interface=Interface(self,self._environment)
        sys.exit(self._app.exec())

    def setAcceleration(self, acceleration): # TODO : Notify toolsbar
        """
        This method is used to change the acceleration of the simulation
        :param acceleration: new acceleration of the simulation
        """
        self._acceleration=acceleration

    def time(self):
        """
        This method is used to get the time elasped since the beginning of the simulation
        :return: the time elapsed [s]
        """
        return self._timeElapsed

    def setAppShown(self,shown):
        self._appShown=shown

    def closeInterface(self):
        if self._appShown:
            self._appShown = False
            self._interface.close()
        # TODO : fermer également l'application ?

    def getAcceleration(self):
        """
        This method is used to get the acceleration of the simulation
        :return: the acceleration of the simulation
        """
        return self._acceleration

    def updateAcceleration(self,sender):
        self._acceleration=sender.getAcceleration()

    def updatePlayState(self,sender):
        self._playState=sender.getPlayState()


