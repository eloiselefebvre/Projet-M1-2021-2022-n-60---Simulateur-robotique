from PyQt5.QtWidgets import QMainWindow

from Object import Object

class Environment(QMainWindow):

    def __init__(self,objects):
        super().__init__()
        self._objects=objects

    def paintEvent(self,event):
        for obj in self._objects:
            obj.paint(self)
        self.update()