from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QToolBar, QLabel, QHBoxLayout, QWidget, QLineEdit

from discoverySimulator.Observable import Observable
from discoverySimulator.config import config
from discoverySimulator.interface.componants.Button import Button, PlayButton
from discoverySimulator.interface.views.PopUp import PopUp


class Toolbar(QToolBar,Observable):

    TOOLSBAR_FIXED_HEIGHT = 42

    ACCELERATION_MIN = 0.1
    ACCELERATION_MAX = 15.0

    def __init__(self):
        super().__init__()
        self.setFixedHeight(self.TOOLSBAR_FIXED_HEIGHT)
        self.setStyleSheet("*{background: #21212f;color:#f0f0f0;border:none;}"
                           "#widget{border-right:1px solid #4D4D6D; margin-top:8px; margin-bottom:8px;}")


        self._acceleration = 1.0
        self._playState = True

        self.setContentsMargins(0,0,0,0)
        self.addWidget(self.createAboutWidget())
        self.addWidget(self.createTimerWidget())
        self.addWidget(self.createAccelerationWidget())
        self.addWidget(self.createPlayPauseWidget())

    def createAboutWidget(self):
        about=QWidget()
        about.setObjectName("widget")
        about_layout=QHBoxLayout(about)

        about_button = Button()
        about_button.setIcon(QIcon(f"{config['ressourcesPath']}/info.svg"))
        about_button.setIconSize(QSize(22, 22))
        about_button.clicked.connect(self.__openPopUp)
        about_layout.addWidget(about_button)

        return about

    def __openPopUp(self):
        popUp = PopUp()

    def createTimerWidget(self):
        timer_icon=QLabel()
        timer_icon.setStyleSheet(f"margin-right:6px; image: url({config['ressourcesPath']}/timer.svg);"
                                 f"image-repeat:no-repeat; image-position:center; image-size:contain;")
        timer_icon.setFixedWidth(22)


        timer = QWidget()
        timer.setObjectName("widget")
        timer_layout=QHBoxLayout(timer)

        timer_layout.setSpacing(0)
        timer_layout.setContentsMargins(12,0,12,0)

        self._timeElapsed=QLabel("0s")

        timer_layout.addWidget(timer_icon)
        timer_layout.addWidget(self._timeElapsed)

        timer_layout.setAlignment(Qt.AlignLeft)

        self._timeElapsed.setFont(QFont("Sanserif", 12))

        return timer

    def createAccelerationWidget(self):
        acceleration=QWidget()
        acceleration.setObjectName("widget")

        acceleration_layout=QHBoxLayout(acceleration)
        acceleration_layout.setSpacing(0)
        acceleration_layout.setContentsMargins(0,0,0,0)

        decrease_button = Button()
        decrease_button.setIcon(QIcon(f"{config['ressourcesPath']}/decreaseAcceleration.svg"))
        decrease_button.clicked.connect(self.__clickedDecreaseAcceleration)

        self._valueAcceleration = QLineEdit()
        self._valueAcceleration.setMaxLength(5)
        self._valueAcceleration.setFont(QFont("Sanserif", 12))
        self._valueAcceleration.setFixedWidth(42)
        self._valueAcceleration.setAlignment(Qt.AlignCenter)
        self._valueAcceleration.editingFinished.connect(self.__inputValueAcceleration)
        self.__accelerationChanged()

        increase_button=Button()
        increase_button.setIcon(QIcon(f"{config['ressourcesPath']}/increaseAcceleration.svg"))
        increase_button.clicked.connect(self.__clickedIncreaseAcceleration)

        acceleration_layout.addWidget(decrease_button)
        acceleration_layout.addWidget(self._valueAcceleration)
        acceleration_layout.addWidget(increase_button)

        acceleration.setFixedWidth(114)

        return acceleration

    def __inputValueAcceleration(self):
        text = self._valueAcceleration.text()
        if text[0]=='x':
            text=text.strip('x')
        try:
            acc=float(text)
            if acc >= self.ACCELERATION_MIN and acc <= self.ACCELERATION_MAX:
                self._acceleration=acc
            if acc > self.ACCELERATION_MAX:
                self._acceleration= self.ACCELERATION_MAX
        except ValueError:
            return
        finally:
            self.__accelerationChanged()

    def __accelerationChanged(self):
        self._acceleration=round(self._acceleration,1)
        self._valueAcceleration.setText(f'x{self._acceleration}')
        self._valueAcceleration.clearFocus()
        self.notifyObservers("accelerationChanged")

    def __clickedDecreaseAcceleration(self):
        self._acceleration-= 0.1 if self._acceleration<=1 else 1.0
        self._acceleration=max(self._acceleration,self.ACCELERATION_MIN)
        self.__accelerationChanged()

    def __clickedIncreaseAcceleration(self):
        self._acceleration += 0.1 if self._acceleration<1 else 1.0
        self._acceleration=min(self._acceleration,self.ACCELERATION_MAX)
        self.__accelerationChanged()

    def getAcceleration(self):
        return self._acceleration

    def createPlayPauseWidget(self):
        self._playPause = PlayButton(self._playState)
        self._playPause.setStyleSheet("margin-left:12px;")
        self._playPause.clicked.connect(self.__togglePlayState)
        return self._playPause

    def getPlayState(self):
        return self._playState

    def __togglePlayState(self):
        self._playState=not self._playState
        self._playPause.setState(self._playState)
        self.notifyObservers("playChanged")

    def updateTimeElapsed(self,sender):
        self._timeElapsed.setText(f"{round(sender.time(),1)}s")

