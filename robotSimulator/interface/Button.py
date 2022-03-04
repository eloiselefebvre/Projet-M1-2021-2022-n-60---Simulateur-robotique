from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from robotSimulator.config import config


class Button(QPushButton):

     def __init__(self):
         super().__init__()
         self.setFlat(True)

class VisibilityButton(Button):

    def __init__(self,visibleObj=True):
        super().__init__()
        self._visibleObj=visibleObj
        self.setFixedWidth(28)
        self.setVisibleIcon(True)

    def setVisibleIcon(self,state):
        if state:
            self.setIcon(QIcon(f"{config['ressourcesPath']}/visible.svg"))
        else:
            self.setIcon(QIcon(f"{config['ressourcesPath']}/invisible.svg"))

    def setVisibleObject(self,visibleObj):
        self._visibleObj=visibleObj
        self.setVisibleIcon()

    def lock(self):
        self.setDisabled(True)
        self.setIcon(QIcon(f"{config['ressourcesPath']}/point.svg"))

    def unlock(self):
        self.setDisabled(False)
        self.setVisibleIcon()




