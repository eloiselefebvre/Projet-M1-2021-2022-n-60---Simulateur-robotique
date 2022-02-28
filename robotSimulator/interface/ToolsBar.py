import PyQt5.Qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QSlider, QPushButton, QLabel

from robotSimulator.config import config

class ToolsBar(QWidget):

    TOOLS_BAR_FIXED_HEIGHT = 60


    def __init__(self,environment,simulation):
        super().__init__()
        self._environment=environment
        self._simulation = simulation

        self._toolsBarLayout=QHBoxLayout()
        self.setLayout(self._toolsBarLayout)
        self.setStyleSheet("background-color: #21212F")
        self._buttonPlay=self.widgetPlayPause()

        self._toolsBarLayout.addWidget(self.widgetTimeElapsed(),60)
        self._toolsBarLayout.addWidget(self._buttonPlay)
        self._toolsBarLayout.addWidget(self.widgetModifyAcceleration())

    def widgetTimeElapsed(self):
        timeElapsedWidget=QWidget()
        timeElapsedWidget.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)
        return timeElapsedWidget

    def widgetPlayPause(self):
        playPauseWidget=QPushButton()
        playPauseWidget.setFixedSize(100,self.TOOLS_BAR_FIXED_HEIGHT)
        playPauseWidget.setFlat(True)

        playPauseWidget.clicked.connect(self.clicked)
        if self._simulation.getPlay()==True:
            playPauseWidget.setIcon(QIcon(f"{config['ressourcesPath']}/pause.svg"))
        else:
            playPauseWidget.setIcon(QIcon(f"{config['ressourcesPath']}/play.svg"))
        return playPauseWidget

    def widgetModifyAcceleration(self):
        modifyAccelerationWidget=QWidget()
        modifyAccelerationWidget.setFixedSize(200,self.TOOLS_BAR_FIXED_HEIGHT)
        modifyAccelerationWidget.setLayout(self.accelerationButtons())

        return modifyAccelerationWidget

    def getHeight(self):
        return self.TOOLS_BAR_FIXED_HEIGHT

    def accelerationButtons(self):
        layout=QHBoxLayout()
        buttonHigh = QPushButton()
        buttonLow = QPushButton()
        buttonHigh.setFlat(True)
        buttonLow.setFlat(True)
        layout.addWidget(buttonLow)
        layout.addWidget(buttonHigh)
        layout.setSpacing(0)

        buttonLow.clicked.connect(self._simulation.decreaseAcceleration)
        buttonLow.setIcon(QIcon(f"{config['ressourcesPath']}/decreaseAcceleration.svg"))
        buttonHigh.setIcon(QIcon(f"{config['ressourcesPath']}/increaseAcceleration.svg"))
        buttonHigh.clicked.connect(self._simulation.increaseAcceleration)

        return layout

    def clicked(self):
        self._simulation.playPause()
        if self._simulation.getPlay()==True:
            self._buttonPlay.setIcon(QIcon(f"{config['ressourcesPath']}/pause.svg"))
        else:
            self._buttonPlay.setIcon(QIcon(f"{config['ressourcesPath']}/play.svg"))



