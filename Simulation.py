import sys
from PyQt5.QtWidgets import QApplication
from Environment import Environment
from Object import Object
import threading

class Simulation:

    def __init__(self):
        self._environment=None
        self._objects=[]

    def addObject(self,obj):
        if isinstance(obj, Object):
            self._objects.append(obj)

    def start(self,program):
        th1=threading.Thread(target=self.simulate)
        th2=threading.Thread(target=program)
        th1.start()
        th2.start()

    def simulate(self):
        app = QApplication([sys.argv])
        self._environment = Environment(self._objects)
        self._environment.setWindowTitle("Spicy Simulator")
        self._environment.showMaximized()
        sys.exit(app.exec())

