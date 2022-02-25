import PyQt5.Qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QSlider, QPushButton, QLabel

from robotSimulator.config import config
from robotSimulator.interface.MenuBar import MenuBar


class ToolsBar(QVBoxLayout):

    TOOLS_BAR_FIXED_HEIGHT = 60

    def __init__(self,environment,simulation):
        super().__init__()
        self._environment=environment
        self._simulation = simulation

        self._searchBarWidget = QWidget()
        self._displayBarWidget = QWidget()

        self._modifyAccelerationWidget=QWidget()
        self._valueModifyAcceleration = QWidget()
        self._playPauseWidget = QWidget()

        self._searchBarLayout=QHBoxLayout()
        self._displayBarLayout=QHBoxLayout()

        self._searchBarWidget.setLayout(self._searchBarLayout)
        self._displayBarWidget.setLayout(self._displayBarLayout)

        self._timeElapsedWidget=self.widgetTimeElapsed()
        self._playPauseWidget = self.widgetPlayPause()
        self._modifyAccelerationWidget = self.widgetModifyAcceleration()

        self._displayBarLayout.addWidget(self._timeElapsedWidget,60)
        self._displayBarLayout.addWidget(self._playPauseWidget,20)
        self._displayBarLayout.addWidget(self._modifyAccelerationWidget,20)
        self._displayBarLayout.setSpacing(0)

        self.addWidget(self._searchBarWidget,50)
        self.addWidget(self._displayBarWidget,50)

        self._menuBarWidget = MenuBar()

        self._searchBarLayout.addWidget(self._menuBarWidget)
        self._searchBarLayout.setSpacing(0)

    def widgetTimeElapsed(self):
        timeElapsedWidget=QWidget()
        timeElapsedWidget.setStyleSheet("background-color: #21212F")
        timeElapsedWidget.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)
        timeElapsedLayout = QVBoxLayout()
        timeElapsedLayout.setSpacing(0)
        timeElapsedWidget.setLayout(timeElapsedLayout)
        return timeElapsedWidget

    def widgetPlayPause(self):
        self._playPauseWidget.setStyleSheet("background-color: #21212F")
        self._playPauseWidget.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)
        playPauseLayout = QVBoxLayout()
        playPauseLayout.setSpacing(0)
        self._playPauseWidget.setLayout(playPauseLayout)

        self._playPauseButtons = QWidget()
        self.playPauseButtons()
        playPauseLayout.addWidget(self._playPauseButtons)
        self._playPauseButtons.setStyleSheet("background-color: #21212F")

        return self._playPauseWidget

    def widgetModifyAcceleration(self):
        self._modifyAccelerationWidget.setStyleSheet("background-color: #21212F")
        self._modifyAccelerationWidget.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)
        modifyAccelerationLayout = QVBoxLayout()
        modifyAccelerationLayout.setSpacing(0)
        self._modifyAccelerationWidget.setLayout(modifyAccelerationLayout)

        # titleModifyAcceleration = QLabel("Acceleration")
        # titleModifyAcceleration.setStyleSheet("background-color: #f0f0f0")
        # modifyAccelerationLayout.addWidget(titleModifyAcceleration)
        # titleModifyAcceleration.setStyleSheet("background-color: #fff")

        self._valueModifyAcceleration =QWidget()
        self.accelerationButtons()
        modifyAccelerationLayout.addWidget(self._valueModifyAcceleration)
        self._valueModifyAcceleration.setStyleSheet("background-color: #21212F")

        return self._modifyAccelerationWidget


    def getHeight(self):
        return self.TOOLS_BAR_FIXED_HEIGHT


    def accelerationButtons(self):
        layout=QHBoxLayout()
        self._valueModifyAcceleration.setLayout(layout)
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


    def playPauseButtons(self):
        layout = QHBoxLayout()
        self._playPauseButtons.setLayout(layout)
        self._buttonPlay = QPushButton()
        self._buttonPlay.setFlat(True)
        layout.addWidget(self._buttonPlay)
        layout.setSpacing(0)

        self._buttonPlay.clicked.connect(self.clicked)
        if self._simulation.getPlay()==True:
            self._buttonPlay.setIcon(QIcon(f"{config['ressourcesPath']}/pause.svg"))
        else:
            self._buttonPlay.setIcon(QIcon(f"{config['ressourcesPath']}/play.svg"))

    def clicked(self):
        self._simulation.playPause()
        if self._simulation.getPlay()==True:
            self._buttonPlay.setIcon(QIcon(f"{config['ressourcesPath']}/pause.svg"))
        else:
            self._buttonPlay.setIcon(QIcon(f"{config['ressourcesPath']}/play.svg"))



