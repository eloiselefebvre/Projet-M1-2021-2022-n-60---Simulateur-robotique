from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from discoverySimulator.config import *


class Button(QPushButton):

    __BUTTON_SIZE = 24
    __ICON_SIZE = 18

    def __init__(self):
         super().__init__()
         self.setFlat(True)

         self.setFixedSize(QSize(Button.__BUTTON_SIZE,Button.__BUTTON_SIZE))
         self.setIconSize(QSize(Button.__ICON_SIZE,Button.__ICON_SIZE))
         self.setStyleSheet("QPushButton{border-radius:2px;}"
                            "QPushButton:hover{background-color:#323247;}"
                            "QPushButton:pressed{background-color:#4C4C68;}")

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

    def __init__(self,visibility=True):
        super().__init__(visibility)
        self.setTrueStateIcon(QIcon(os.path.join(config['ressourcesPath'],'states','visible.svg')))
        self.setFalseStateIcon(QIcon(os.path.join(config['ressourcesPath'],'states','invisible.svg')))

    def lock(self):
        self.setDisabled(True)
        self.setIcon(QIcon(os.path.join(config['ressourcesPath'],'states','point.svg')))

    def unlock(self):
        self.setDisabled(False)
        self.setStateIcon()

class LockButton(ToggleButton):

    def __init__(self,lock=False):
        super().__init__(lock)
        self.setTrueStateIcon(QIcon(os.path.join(config['ressourcesPath'],'states','lock.svg')))
        self.setFalseStateIcon(QIcon(os.path.join(config['ressourcesPath'],'states','unlock.svg')))

class PlayButton(ToggleButton):

    def __init__(self,play=False):
        super().__init__(play)
        self.setTrueStateIcon(QIcon(os.path.join(config['ressourcesPath'],'toolbar','pause.svg')))
        self.setFalseStateIcon(QIcon(os.path.join(config['ressourcesPath'],'toolbar','play.svg')))