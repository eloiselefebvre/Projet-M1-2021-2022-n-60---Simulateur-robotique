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
        self.__environment=environment
        self.__app = None
        self.__interface=None
        self.__appShown = False
        self.__acceleration = 1
        self.__timeElapsed = 0.0
        self.__playState=True

    def getAcceleration(self) -> float:
        """
        This method is used to get the acceleration of the simulation
        :return: the acceleration of the simulation
        """
        return self.__acceleration

    def time(self) -> float:
        """
        This method is used to get the time elasped since the beginning of the simulation
        :return: time elapsed [s]
        """
        return self.__timeElapsed

    def setAcceleration(self, acceleration:float): # TODO : Notify toolsbar
        """
        This method is used to change the acceleration of the simulation
        :param acceleration: new acceleration of the simulation
        """
        self.__acceleration=acceleration

    def setAppShown(self,shown:bool):
        self.__appShown=shown

    def run(self):
        """
        This method allows to run the simulation
        """
        th = threading.Thread(target=self.__run)
        th.start()

    def showInterface(self):
        """
        This method allows to show the interface where the simulation takes place
        """
        if self.__environment is not None and not self.__appShown:
            th=threading.Thread(target=self.__startApplication)
            th.start()
            self.__appShown = True

    def closeInterface(self):
        if self.__appShown:
            self.__appShown = False
            self.__interface.close()
        # TODO : fermer également l'application ?

    # NOTIFY METHOD
    def updateAcceleration(self,sender):
        self.__acceleration=sender.getAcceleration()

    # NOTIFY METHOD
    def updatePlayState(self,sender):
        self.__playState=sender.getPlayState()

    def __run(self):
        start_update = time.time()
        while True:
            current=time.time()
            if current - start_update > config["update_time_step"] / self.__acceleration:
                start_update = current

                # ROBOT UPDATE
                if self.__playState:
                    self.__timeElapsed += config["update_time_step"] * self.__acceleration

                    self.notifyObservers("timeChanged")
                    for obj in self.__environment.getObjects():
                        if hasattr(obj, "move"):
                            obj.move()

                # SENSOR UPDATE
                for sensor in self.__environment.getSensors():
                    if hasattr(sensor, "refresh"):
                        sensor.refresh()
            time.sleep(self.MINIMUM_TIME_STEP)

    def __startApplication(self):
        self.__app = QApplication([sys.argv])
        self.__interface=Interface(self, self.__environment)
        sys.exit(self.__app.exec())

