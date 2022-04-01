import sys
from PyQt5.QtWidgets import QApplication
from discoverySimulator.interface.views.Interface import Interface
from discoverySimulator.Observable import Observable
import threading
import time
from discoverySimulator.config import *

class Simulation(Observable):

    """ The Simulation class provides a simulation."""

    __MINIMUM_TIME_STEP = 0.001

    def __init__(self,environment=None):
        """ Constructs a new simulation.
        @param environment  environment where the simulation will take place."""
        super().__init__()
        self.__environment=environment
        self.__app = None
        self.__interface=None
        self.__appShown = False
        self.__acceleration = 1
        self.__timeElapsed = 0.0
        self.__playState=True
        self.__hasBeenRefreshed=False

    # SETTERS
    def setAcceleration(self, acceleration:float): # TODO : Notify toolsbar
        """ Sets the acceleration of the simulation.
        @param acceleration  New acceleration of the simulation"""
        self.__acceleration=acceleration

    def setAppShown(self,shown:bool):
        self.__appShown=shown

    # GETTERS
    def getAcceleration(self) -> float:
        """ Returns the acceleration of the simulation."""
        return self.__acceleration

    def time(self) -> float:
        """ Returns the time elapsed since the beginning of the simulation. [s]"""
        return self.__timeElapsed

    def run(self):
        """ Runs the simulation."""
        th = threading.Thread(target=self.__run)
        th.start()

    def showInterface(self):
        """ Shows the interface where the simulation takes place."""
        if self.__environment is not None and not self.__appShown:
            th=threading.Thread(target=self.__startApplication)
            th.start()
            self.__appShown = True

    def closeInterface(self):
        """ Closes the interface."""
        if self.__appShown:
            self.__appShown = False
            self.__interface.close()
        # TODO : fermer également l'application ?

    def sleep(self,delay):
        start = time.time()
        while time.time()-start<delay/self.__acceleration:
            time.sleep(0.001)

    def sync(self):
        while not self.__hasBeenRefreshed:
            time.sleep(0.001)
        self.__hasBeenRefreshed=False

    # NOTIFY METHOD
    def updateAcceleration(self,sender):
        self.__acceleration=sender.getAcceleration()

    # NOTIFY METHOD
    def updatePlayState(self,sender):
        self.__playState=sender.getPlayState()

    def __run(self):
        start = time.time()
        while True:
            # ROBOT UPDATE
            current = time.time()
            if self.__playState:
                config["real_update_time_step"]=(current - start)*self.__acceleration
                self.__timeElapsed += config["real_update_time_step"]
            start=time.time()
            if self.__playState:
                self.notifyObservers("timeChanged")
                for obj in self.__environment.getObjects():
                    if hasattr(obj, "move"):
                        obj.move()
                self.__hasBeenRefreshed=True

            # SENSOR UPDATE
            for sensor in self.__environment.getSensors():
                if hasattr(sensor, "refresh"):
                    sensor.refresh()

            time.sleep(self.__MINIMUM_TIME_STEP)

    def __startApplication(self):
        self.__app = QApplication([sys.argv])
        self.__interface=Interface(self, self.__environment)
        sys.exit(self.__app.exec())

