import sys
from PyQt5.QtWidgets import QApplication
from robotSimulator.Interface import Interface
import threading

class Simulation:

    def __init__(self,environment=None):
        self._environment=environment
        self._shown = False

    def showInterface(self):
        if self._environment is not None and not self._shown:
            th=threading.Thread(target=self.__startApplication,args=(self._environment,))
            th.start()
            self._shown = True

    def __startApplication(self,environment):
        app = QApplication([sys.argv])
        myInterface = Interface(environment)
        sys.exit(app.exec())

