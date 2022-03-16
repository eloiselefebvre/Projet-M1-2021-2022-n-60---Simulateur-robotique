from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from discoverySimulator.config import config


class Button(QPushButton):
     def __init__(self):
         super().__init__()
         self.setFlat(True)
         self.setFixedWidth(28)
         self.setIconSize(QSize(18, 18))

class ToggleButton(Button):
    def __init__(self,state=True):
        super().__init__()
        self._state=state
        self._trueStateIcon=None
        self._falseStateIcon=None

    def setStateIcon(self):
        if self._state:
            if self._trueStateIcon is not None:
                self.setIcon(self._trueStateIcon)
        else:
            if self._falseStateIcon is not None:
                self.setIcon(self._falseStateIcon)

    def setState(self,state):
        self._state=state
        self.setStateIcon()

    def setTrueStateIcon(self,icon):
        self._trueStateIcon=icon
        self.setStateIcon()

    def setFalseStateIcon(self,icon):
        self._falseStateIcon=icon
        self.setStateIcon()


class VisibilityButton(ToggleButton):

    def __init__(self,visibiliy=True):
        super().__init__(visibiliy)
        self.setTrueStateIcon(QIcon(f"{config['ressourcesPath']}/visible.svg"))
        self.setFalseStateIcon(QIcon(f"{config['ressourcesPath']}/invisible.svg"))

    def lock(self):
        self.setDisabled(True)
        self.setIcon(QIcon(f"{config['ressourcesPath']}/point.svg"))

    def unlock(self):
        self.setDisabled(False)
        self.setStateIcon()

class LockButton(ToggleButton):

    def __init__(self,lock=False):
        super().__init__(lock)
        self.setTrueStateIcon(QIcon(f"{config['ressourcesPath']}/lock.svg"))
        self.setFalseStateIcon(QIcon(f"{config['ressourcesPath']}/unlock.svg"))

class PlayButton(ToggleButton):

    def __init__(self,play=False):
        super().__init__(play)
        self.setTrueStateIcon(QIcon(f"{config['ressourcesPath']}/pause.svg"))
        self.setFalseStateIcon(QIcon(f"{config['ressourcesPath']}/play.svg"))