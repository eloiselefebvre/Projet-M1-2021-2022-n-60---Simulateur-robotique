from PyQt5.QtWidgets import QMainWindow

class Interface(QMainWindow):
    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self.setWindowTitle("Spicy Simulator")
        self.showMaximized()

    def paintEvent(self,event):
        for obj in self._environment.getObjects():
            obj.paint(self)
        self.update()