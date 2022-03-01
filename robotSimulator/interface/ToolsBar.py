from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QLabel, QAction, QWidgetAction, QToolBar

from robotSimulator.config import config

class ToolsBar(QToolBar):

    TOOLS_BAR_FIXED_HEIGHT = 50
    BUTTON_FIXED_WIDTH = 150

    def __init__(self,environment,simulation,interface):
        super().__init__()
        self._environment=environment
        self._simulation = simulation
        self._interface=interface

        self._tb = self._interface.addToolBar("ToolBar")
        self._tb.setStyleSheet("background: #21212f")

        self._tb.setFixedHeight(70)
        self._tb.addAction(self.decreaseAcceleration())
        self._tb.addAction(self.valueAcceleration())
        self._tb.addAction(self.increaseAcceleration())
        self._playPauseAction=self.playPause()
        self._tb.addAction(self._playPauseAction)
        self._tb.setMovable(False)

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
        self._valueAcceleration = QLabel("x"+str(self._simulation.getAcceleration()))
        valueAccelerationWidget.setDefaultWidget(self._valueAcceleration)
        self._valueAcceleration.setFont(QFont("Sanserif",15))
        self._valueAcceleration.setStyleSheet("color: #f0f0f0")
        return valueAccelerationWidget

    def playPause(self):
        self._playPause = QAction(QIcon(f"{config['ressourcesPath']}/pause.svg"),"IncreaseAcceleration",self._interface)
        self._playPause.triggered.connect(self.clicked)
        return self._playPause

    def setAccelerationLabel(self):
        self._valueAcceleration.setText("x"+str(round(self._simulation.getAcceleration(),1)))

    def clickedIncreaseAcceleration(self):
        self._simulation.increaseAcceleration()
        self.setAccelerationLabel()

    def clickedDecreaseAcceleration(self):
        self._simulation.decreaseAcceleration()
        self.setAccelerationLabel()

    def clicked(self):
        self._simulation.playPause()
        if self._simulation.getPlay():
            icon =QIcon(f"{config['ressourcesPath']}/pause.svg")
        else:
            icon =QIcon(f"{config['ressourcesPath']}/play.svg")
        self._playPauseAction.setIcon(icon)




