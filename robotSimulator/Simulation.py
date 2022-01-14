import sys
from PyQt5.QtWidgets import QApplication
from Environment import Environment
from Interface import Interface
from Object import Object
import threading

class Simulation:

    def __init__(self,environment=None):
        self._environment=environment
        self._shown = False

    def show(self):
        if self._environment is not None and not self._shown:
            th=threading.Thread(target=self.showInterface,args=(self._environment,))
            th.start()
            self._shown = True

    def showInterface(self,environment):
        app = QApplication([sys.argv])
        myInterface = Interface(environment)
        sys.exit(app.exec())

