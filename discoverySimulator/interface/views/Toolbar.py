from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QToolBar, QLabel, QHBoxLayout, QWidget, QLineEdit, QWidgetAction
from discoverySimulator.Observable import Observable
from discoverySimulator.config import config
from discoverySimulator.interface.components.Button import Button, PlayButton
from discoverySimulator.interface.views.PopUp import PopUp


class Toolbar(QToolBar,Observable):

    TOOLSBAR_FIXED_HEIGHT = 48

    ACCELERATION_MIN = 0.1
    ACCELERATION_MAX = 15.0

    def __init__(self):
        super().__init__()
        self.setFixedHeight(self.TOOLSBAR_FIXED_HEIGHT)
        self.setStyleSheet("*{background-color: #21212f;color:#f0f0f0;border:none;}"
                           "#widget{border-right:1px solid #4D4D6D; margin-top:8px; margin-bottom:8px;}"
                           "QPushButton:hover{background-color:#323247;}"
                           "QPushButton:pressed{background-color:#4C4C68;}")
        self._acceleration = 1.0
        self._playState = True
        self._robotTitleWidget=None
        self._pathFollowingWidget=None

        self.setContentsMargins(0,0,0,0)
        self.addWidget(self.createAboutWidget())

        self.addAction(self.createSectionTitleWidget("Simulation"))
        self.addWidget(self.createTimerWidget())
        self.addWidget(self.createAccelerationWidget())
        self.addWidget(self.createPlayPauseWidget())

        self._robotTitleWidget = self.createSectionTitleWidget("Robot")
        self._pathFollowingWidget=self.pathFollowingButton()
        self._robotSelected=None
        self._previousSender=None

    def createSectionTitleWidget(self,name=""):
        labelWidget = QWidgetAction(self)
        label=QLabel(name+":")
        fnt=QFont("Sanserif",12)
        label.setFont(fnt)
        label.setStyleSheet("color:#fff; border-left:1px solid #4D4D6D;")
        label.setContentsMargins(8,0,0,0)
        labelWidget.setDefaultWidget(label)
        return labelWidget

    def createAboutWidget(self):
        about=QWidget()
        about_layout=QHBoxLayout(about)

        about_layout.setSpacing(0)
        about.setContentsMargins(4, 0, 4, 0)

        about_button = Button()
        about_button.setIcon(QIcon(f"{config['ressourcesPath']}/toolbar/info.svg"))
        about_button.setIconSize(QSize(22, 22))
        about_button.clicked.connect(self.__openPopUp)
        about_button.setToolTip("About")
        about_layout.addWidget(about_button)

        about.setFixedHeight(self.TOOLSBAR_FIXED_HEIGHT)

        return about

    def __openPopUp(self):
        PopUp()

    def createTimerWidget(self):
        timer_icon=QLabel()
        timer_icon.setStyleSheet(f"image: url({config['ressourcesPath']}/toolbar/timer.svg);"
                                 f"image-repeat:no-repeat; image-position:center; image-size:contain;")
        timer_icon.setFixedWidth(16)

        timer = QWidget()
        timer.setObjectName("widget")
        timer_layout=QHBoxLayout(timer)

        timer_layout.setSpacing(0)
        timer.setContentsMargins(4,0,4,0)

        self._timeElapsed=QLabel("0s")
        self._timeElapsed.setStyleSheet("margin-left:8px;")

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
        acceleration.setContentsMargins(4,0,4,0)

        decrease_button = Button()
        decrease_button.setIcon(QIcon(f"{config['ressourcesPath']}/toolbar/decreaseAcceleration.svg"))
        decrease_button.setToolTip("Decrease Acceleration")
        decrease_button.clicked.connect(self.__clickedDecreaseAcceleration)

        self._valueAcceleration = QLineEdit()
        self._valueAcceleration.setMaxLength(5)
        self._valueAcceleration.setFont(QFont("Sanserif", 12))
        self._valueAcceleration.setFixedWidth(42)
        self._valueAcceleration.setAlignment(Qt.AlignCenter)
        self._valueAcceleration.editingFinished.connect(self.__inputValueAcceleration)
        self.__accelerationChanged()

        increase_button=Button()
        increase_button.setIcon(QIcon(f"{config['ressourcesPath']}/toolbar/increaseAcceleration.svg"))
        increase_button.setToolTip("Increase Acceleration")
        increase_button.clicked.connect(self.__clickedIncreaseAcceleration)

        acceleration_layout.addWidget(decrease_button)
        acceleration_layout.addWidget(self._valueAcceleration)
        acceleration_layout.addWidget(increase_button)

        acceleration.setFixedWidth(132)

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
        play = QWidget()
        play_layout=QHBoxLayout(play)
        play_layout.setSpacing(0)
        play.setContentsMargins(4, 0, 4, 0)

        self._playPause = PlayButton(self._playState)
        self._playPause.setToolTip("Pause" if self._playState else "Play")
        self._playPause.clicked.connect(self.__togglePlayState)

        play_layout.addWidget(self._playPause)
        return play

    def getPlayState(self):
        return self._playState

    def __togglePlayState(self):
        self._playState=not self._playState
        self._playPause.setToolTip("Pause" if self._playState else "Play")
        self._playPause.setState(self._playState)
        self.notifyObservers("playChanged")

    def updateTimeElapsed(self,sender):
        time=sender.time()
        hours=int(time//3600)
        time-=hours*3600
        minutes=int(time//60)
        time-=minutes*60
        seconds=time

        str=""
        if hours>0:
            str+=f"{hours}h"
        if minutes>0 or hours>0:
            str+=f"{'0' if minutes<10 and hours>0 else ''}{minutes}min"
        str+=f"{'0' if seconds<10 and (minutes>0 or hours>0) else ''}{round(seconds,1) if minutes==0 else int(seconds)}s"
        self._timeElapsed.setText(str)

    def robotSelected(self,sender):
        if sender.isSelected():
            self._robotSelected=sender
            self.addAction(self._robotTitleWidget)
            self.addAction(self._pathFollowingWidget)
        else:
            self.removeAction(self._robotTitleWidget)
            self.removeAction(self._pathFollowingWidget)

    def pathFollowingButton(self):
        widget=QWidgetAction(self)
        self._pathFollowingButton = Button()
        widget.setDefaultWidget(self._pathFollowingButton)
        self._pathFollowingButton.setIcon(QIcon(f"{config['ressourcesPath']}/toolbar/goTo.svg"))
        self._pathFollowingButton.setToolTip("Go To")
        self._pathFollowingButton.clicked.connect(self.__clickedFollowPath)
        return widget

    def __clickedFollowPath(self):
        self._pathFollowingButton.setDown(True)
        self.notifyObservers('followPathSelected')

    def getRobotSelected(self):
        return self._robotSelected

