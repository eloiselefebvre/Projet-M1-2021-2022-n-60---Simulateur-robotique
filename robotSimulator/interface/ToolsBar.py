from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QLabel, QAction, QWidgetAction, QToolBar, QPushButton, QLineEdit, QTextEdit, QMenu, \
    QComboBox

from robotSimulator.Observable import Observable
from robotSimulator.config import config

class ToolsBar(QToolBar,Observable):

    TOOLS_BAR_FIXED_HEIGHT = 50
    BUTTON_FIXED_WIDTH = 150

    def __init__(self,environment,interface):
        super().__init__()
        self._environment=environment
        self._interface=interface
        self._acceleration = 1

        self._tb = self._interface.addToolBar("ToolBar")
        self._tb.setStyleSheet("background: #21212f")

        self._tb.setFixedHeight(70)
        self._tb.addAction(self.decreaseAcceleration())
        self._tb.addAction(self.valueAcceleration())
        self._tb.addAction(self.increaseAcceleration())
        self._playPauseAction=self.playPause()
        self._tb.addAction(self._playPauseAction)

        self._tb.setMovable(False)

        self._playState=True

    def increaseAcceleration(self):
        increaseAcceleration=QAction(QIcon(f"{config['ressourcesPath']}/increaseAcceleration.svg"),"IncreaseAcceleration",self._interface)
        increaseAcceleration.triggered.connect(self.clickedIncreaseAcceleration)
        return increaseAcceleration

    def decreaseAcceleration(self):
        decreaseAcceleration=QAction(QIcon(f"{config['ressourcesPath']}/decreaseAcceleration.svg"),"DecreaseAcceleration",self._interface)
        decreaseAcceleration.triggered.connect(self.clickedDecreaseAcceleration)
        return decreaseAcceleration

    def valueAcceleration(self):
        valueAccelerationWidget=QWidgetAction(self)
        self._valueAcceleration = QLineEdit("x"+str(self._acceleration))

        valueAccelerationWidget.setDefaultWidget(self._valueAcceleration)
        self._valueAcceleration.returnPressed.connect(self.inputValueAcceleration)

        self._valueAcceleration.setStyleSheet("border: none")
        self._valueAcceleration.setFont(QFont("Sanserif",15))
        self._valueAcceleration.setStyleSheet("color: #f0f0f0")
        self._valueAcceleration.setFixedWidth(70)
        return valueAccelerationWidget

    def inputValueAcceleration(self):
        text = self._valueAcceleration.text()
        if text[0]=='x':
            text=text.rstrip(text[0])
        if text.isnumeric():
            self._acceleration=(int(text))
            self.accelerationChanged()

    def playPause(self):
        self._playPause = QAction(QIcon(f"{config['ressourcesPath']}/pause.svg"),"Play/Pause",self._interface)
        self._playPause.triggered.connect(self.clickedPlayPause)
        return self._playPause

    def lockUnlock(self):
        self._lockUnlock = QAction(QIcon(f"{config['ressourcesPath']}/unlock.svg"),"Lock/Unlock",self._interface)
        self._lockUnlock.triggered.connect(self.clickedLockUnlock)
        return self._lockUnlock

    def clickedIncreaseAcceleration(self):
        if self._acceleration<1:
            pas = 0.1
            self._acceleration += pas
        else:
            pas=1
            self._acceleration += pas
        self.accelerationChanged()

    def clickedDecreaseAcceleration(self):

        if self._acceleration<=1:
            pas = 0.1
            if self._acceleration-pas > 0:
                self._acceleration -= pas
        else:
            pas=1
            self._acceleration -= pas
        self.accelerationChanged()

    def accelerationChanged(self):
        self._valueAcceleration.setText("x"+str(round(self._acceleration,1)))
        self.notifyObservers("accelerationChanged")

    def getAcceleration(self):
        return self._acceleration

    def clickedPlayPause(self): # TODO : Revoir avec composant Button
        self.togglePlayState()
        if self._playState:
            icon =QIcon(f"{config['ressourcesPath']}/pause.svg")
        else:
            icon =QIcon(f"{config['ressourcesPath']}/play.svg")
        self._playPauseAction.setIcon(icon)

    def togglePlayState(self):
        self._playState=not self._playState
        self.notifyObservers("playChanged")

    def getPlayState(self):
        return self._playState
