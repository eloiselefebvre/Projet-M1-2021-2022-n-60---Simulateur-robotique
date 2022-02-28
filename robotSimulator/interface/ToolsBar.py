import PyQt5.Qt
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QSlider, QPushButton, QLabel
from PyQt5.uic.properties import QtCore

from robotSimulator.config import config

class ToolsBar(QWidget):

    TOOLS_BAR_FIXED_HEIGHT = 50
    BUTTON_FIXED_WIDTH = 150

    def __init__(self,environment,simulation):
        super().__init__()
        self._environment=environment
        self._simulation = simulation

        self._toolsBarLayout=QHBoxLayout()
        self.setLayout(self._toolsBarLayout)
        self._buttonPlay=self.widgetPlayPause()
        self.setStyleSheet("background-color: #21212F")

        self._accelerationLabelWidget = QLabel("x"+str(self._simulation.getAcceleration()))
        # self._accelerationLabelWidget.setAlignment(QtCore.Qt.AlignCenter)

        self._toolsBarLayout.addWidget(self.widgetTimeElapsed(),60)
        self._toolsBarLayout.addWidget(self._buttonPlay)
        self._toolsBarLayout.addWidget(self.decreaseAccelerationButton())
        self._toolsBarLayout.addWidget(self.acceleration())
        self._toolsBarLayout.addWidget(self.increaseAccelerationButton())

    def widgetTimeElapsed(self):
        timeElapsedWidget=QWidget()
        timeElapsedWidget.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)
        return timeElapsedWidget

    def widgetPlayPause(self):
        playPauseWidget=QPushButton()
        playPauseWidget.setFixedSize(self.BUTTON_FIXED_WIDTH,self.TOOLS_BAR_FIXED_HEIGHT)
        playPauseWidget.setFlat(True)
        playPauseWidget.setIconSize(QSize(30,30))
        playPauseWidget.clicked.connect(self.clicked)
        if self._simulation.getPlay()==True:
            playPauseWidget.setIcon(QIcon(f"{config['ressourcesPath']}/pause.svg"))
        else:
            playPauseWidget.setIcon(QIcon(f"{config['ressourcesPath']}/play.svg"))
        return playPauseWidget

    def getHeight(self):
        return self.TOOLS_BAR_FIXED_HEIGHT

    def decreaseAccelerationButton(self):
        buttonLow = QPushButton()
        buttonLow.setFlat(True)
        buttonLow.setStyleSheet('QPushButton {background-color: #21212F; color: #21212F;}')
        buttonLow.clicked.connect(self.clickedDecreaseAcceleration)
        buttonLow.setIcon(QIcon(f"{config['ressourcesPath']}/decreaseAcceleration.svg"))
        buttonLow.setIconSize(QSize(30,30))
        buttonLow.setFixedSize(self.BUTTON_FIXED_WIDTH//2,self.TOOLS_BAR_FIXED_HEIGHT)
        return buttonLow

    def increaseAccelerationButton(self):
        buttonHigh = QPushButton()
        buttonHigh.setFlat(True)
        buttonHigh.setStyleSheet('QPushButton {background-color: #21212F; color: #21212F;}')
        buttonHigh.setIcon(QIcon(f"{config['ressourcesPath']}/increaseAcceleration.svg"))
        buttonHigh.setIconSize(QSize(30,30))
        buttonHigh.clicked.connect(self.clickedIncreaseAcceleration)
        buttonHigh.setFixedSize(self.BUTTON_FIXED_WIDTH//2,self.TOOLS_BAR_FIXED_HEIGHT)
        return buttonHigh

    def acceleration(self):
        self._accelerationLabelWidget.setFixedSize(self.BUTTON_FIXED_WIDTH//3,self.TOOLS_BAR_FIXED_HEIGHT)
        self._accelerationLabelWidget.setFont(QFont("Sanserif",18))
        self._accelerationLabelWidget.setStyleSheet("color:#f9f9f9")
        return self._accelerationLabelWidget

    def setAccelerationLabel(self):
        self._accelerationLabelWidget.setText("x"+str(round(self._simulation.getAcceleration(),1)))

    def clickedIncreaseAcceleration(self):
        self._simulation.increaseAcceleration()
        self.setAccelerationLabel()

    def clickedDecreaseAcceleration(self):
        self._simulation.decreaseAcceleration()
        self.setAccelerationLabel()

    def clicked(self):
        self._simulation.playPause()
        if self._simulation.getPlay()==True:
            self._buttonPlay.setIcon(QIcon(f"{config['ressourcesPath']}/pause.svg"))
        else:
            self._buttonPlay.setIcon(QIcon(f"{config['ressourcesPath']}/play.svg"))
