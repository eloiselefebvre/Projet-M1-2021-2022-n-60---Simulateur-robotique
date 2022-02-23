from PyQt5.QtWidgets import QWidget


class Scene(QWidget):

    def __init__(self,environment):
        super().__init__()
        self._environment = environment

    def paintEvent(self,event):
        for obj in self._environment.getObjects():
            obj.paint(self)
        self.update()



