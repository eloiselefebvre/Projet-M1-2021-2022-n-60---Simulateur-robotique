from PyQt5.QtWidgets import QMainWindow

class Environment(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot Simulator")
        self.setStyleSheet("background:#f3f3f3")
        self._objects=[]
        self.showMaximized()

    def addObject(self, object):
        self._objects.append(object)

    def paintEvent(self,event):
        for object in self._objects:
            object.draw(self)
