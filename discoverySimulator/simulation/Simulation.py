import sys
from PyQt5.QtWidgets import QApplication
from discoverySimulator.interface.views.Interface import Interface
from discoverySimulator.Observable import Observable
import threading
import time
from discoverySimulator.config import *

class Simulation(Observable):

    """ The Simulation class provides a simulation."""

    __MINIMUM_TIME_STEP = 1/60

    __ACCELERATION_MIN = 0.1
    __ACCELERATION_MAX = 15.0

    def __init__(self,environment=None):
        """ Constructs a new simulation.
        @param environment  environment where the simulation will take place."""
        super().__init__()
        self.__environment=environment
        self.__app = None
        self.__appShown = False
        self.__acceleration = 1.0
        self.__timeElapsed = 0.0
        self.__playState=True
        self.__hasBeenRefreshed=False

        self.__runThread=None

    # SETTERS
    def setAcceleration(self, acceleration:float):
        """ Sets the acceleration of the simulation.
        @param acceleration  New acceleration of the simulation"""
        try:
            acceleration=float(acceleration)
            if self.__ACCELERATION_MIN <= acceleration <= self.__ACCELERATION_MAX:
                self.__acceleration = acceleration
            if acceleration > self.__ACCELERATION_MAX:
                self.__acceleration = self.__ACCELERATION_MAX
        except ValueError:
            return
        finally:
            self.__accelerationChanged()

    def setPlay(self,state:bool):
        self.__playState=state
        self.__playStateChanged()

    def togglePlayState(self):
        self.__playState=not self.__playState
        self.__playStateChanged()

    def __playStateChanged(self):
        self.notifyObservers("playStateChanged")

    def setAppShown(self,shown:bool):
        self.__appShown=shown
        if not self.__appShown:
            self.clearObserverCallback()

    # GETTERS
    def getAcceleration(self) -> float:
        """ Returns the acceleration of the simulation."""
        return self.__acceleration

    def getPlayState(self) -> bool:
        return self.__playState

    def time(self) -> float:
        """ Returns the time elapsed since the beginning of the simulation. [s]"""
        return self.__timeElapsed

    def run(self):
        """ Runs the simulation."""
        self.stop()
        self.__runThread = threading.Thread(target=self.__run)
        self.__runThread.start()

    def stop(self):
        if self.__runThread is not None:
            self.__runThread.do_run=False
            self.__runThread.join()

    def showInterface(self):
        """ Shows the interface where the simulation takes place."""
        if self.__environment is not None and not self.__appShown:
            self.__appThread=threading.Thread(target=self.__startApplication)
            self.__appThread.start()
            self.__appShown = True

    def closeInterface(self):
        """ Closes the interface."""
        if self.__appShown:
            self.__app.exit(0)
            self.__appThread.join()
            self.setAppShown(False)

    def sleep(self,delay):
        start = time.time()
        while time.time()-start<delay/self.__acceleration:
            time.sleep(0.001)

    def sync(self):
        while not self.__hasBeenRefreshed:
            time.sleep(0.001)
        self.__hasBeenRefreshed=False

    def __run(self):
        start = time.time()
        while getattr(self.__runThread, "do_run", True):
            # ROBOT UPDATE
            current = time.time()
            if self.__playState:
                config["real_update_time_step"]=(current - start)*self.__acceleration
                self.__timeElapsed += config["real_update_time_step"]
                self.notifyObservers("timeChanged")
            start=time.time()
            if self.__playState:
                for obj in self.__environment.getObjects():
                    if hasattr(obj, "move"):
                        obj.move()
                self.__hasBeenRefreshed=True

            # SENSOR UPDATE
            for sensor in self.__environment.getSensors():
                if hasattr(sensor, "refresh"):
                    sensor.refresh()

            self.sleep(self.__MINIMUM_TIME_STEP)

    def __startApplication(self):
        self.__app = QApplication(sys.argv)
        interface=Interface(self, self.__environment)
        self.__app.exec_()

    def __accelerationChanged(self):
        self.__acceleration = round(self.__acceleration, 1)
        self.notifyObservers("accelerationChanged")

    def decreaseAcceleration(self):
        self.__acceleration -= 0.1 if self.__acceleration <= 1 else 1.0
        self.__acceleration = max(self.__acceleration, self.__ACCELERATION_MIN)
        self.__accelerationChanged()

    def increaseAcceleration(self):
        self.__acceleration += 0.1 if self.__acceleration < 1 else 1.0
        self.__acceleration = min(self.__acceleration, self.__ACCELERATION_MAX)
        self.__accelerationChanged()

    def setAccelerationFromString(self,acceleration):
        if acceleration[0] == 'x':
            acceleration = acceleration.strip('x')
        self.setAcceleration(acceleration)

