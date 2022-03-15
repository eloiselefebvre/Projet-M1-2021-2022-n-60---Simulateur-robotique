from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QAction, QWidgetAction, QToolBar, QLineEdit, QLabel, QHBoxLayout, QWidget
from robotSimulator.Observable import Observable
from robotSimulator.config import config
from robotSimulator.interface.views.PopUp import PopUp


class ToolsBar(QToolBar,Observable):

    TOOLS_BAR_FIXED_HEIGHT = 48

    ACCELERATION_MAX = 20.0
    ACCELERATION_MIN = 0.1

    def __init__(self,environment,interface):
        super().__init__()
        self._environment=environment
        self._interface=interface
        self._acceleration = 1.0

        self._tb = self._interface.addToolBar("ToolBar")
        self._tb.setStyleSheet("*{background: #21212f;color:#f0f0f0;border:none;}"
                               "QToolBar::separator{background-color: #4D4D6D; width: 1px; margin: 0 12px;}")

        self._tb.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)

        self._tb.addAction(self.popUp())
        self._tb.addSeparator()
        self._tb.addAction(self.timeElapsed())
        self._tb.addSeparator()
        self._tb.addAction(self.createTimerWidget())
        self._tb.addSeparator()
        self._tb.addAction(self.decreaseAcceleration())
        self._tb.addAction(self.valueAcceleration())
        self._tb.addAction(self.increaseAcceleration())
        self._tb.addSeparator()
        self._playPauseAction=self.playPause()
        self._tb.addAction(self._playPauseAction)
        self._tb.setMovable(False)

        self._playState=True

    def popUp(self):
        widget = QAction(QIcon(f"{config['ressourcesPath']}/info.svg"), "Informations", self._interface)
        widget.triggered.connect(self.openPopUp)
        return widget

    def openPopUp(self):
        popUp = PopUp()

    def increaseAcceleration(self):
        increaseAcceleration=QAction(QIcon(f"{config['ressourcesPath']}/increaseAcceleration.svg"),"Increase Acceleration",self._interface)
        increaseAcceleration.triggered.connect(self.clickedIncreaseAcceleration)
        return increaseAcceleration

    def decreaseAcceleration(self):
        decreaseAcceleration=QAction(QIcon(f"{config['ressourcesPath']}/decreaseAcceleration.svg"),"Decrease Acceleration",self._interface)
        decreaseAcceleration.triggered.connect(self.clickedDecreaseAcceleration)
        return decreaseAcceleration

    def valueAcceleration(self):
        valueAccelerationWidget=QWidgetAction(self)
        self._valueAcceleration = QLineEdit()

        valueAccelerationWidget.setDefaultWidget(self._valueAcceleration)
        self._valueAcceleration.returnPressed.connect(self.inputValueAcceleration)

        self._valueAcceleration.setFont(QFont("Sanserif",15))
        self._valueAcceleration.setFixedWidth(56)
        self._valueAcceleration.setAlignment(Qt.AlignCenter)
        self.accelerationChanged()
        return valueAccelerationWidget

    def inputValueAcceleration(self):
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
            self.accelerationChanged()

    def clickedIncreaseAcceleration(self):
        self._acceleration += 0.1 if self._acceleration<1 else 1.0
        self._acceleration=min(self._acceleration,self.ACCELERATION_MAX)
        self.accelerationChanged()

    def clickedDecreaseAcceleration(self):
        self._acceleration-= 0.1 if self._acceleration<=1 else 1.0
        self._acceleration=max(self._acceleration,self.ACCELERATION_MIN)
        self.accelerationChanged()

    def accelerationChanged(self):
        self._acceleration=round(self._acceleration,1)
        self._valueAcceleration.setText(f'x{self._acceleration}')
        self._valueAcceleration.clearFocus()
        self.notifyObservers("accelerationChanged")

    def getAcceleration(self):
        return self._acceleration

    def playPause(self):
        self._playPause = QAction(QIcon(f"{config['ressourcesPath']}/pause.svg"),"Play/Pause",self._interface)
        self._playPause.triggered.connect(self.clickedPlayPause)
        return self._playPause

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

    def createTimerWidget(self):
        timer_icon=QLabel()
        timer_icon.setPixmap(QPixmap(f"{config['ressourcesPath']}/timer.svg"))
        timer_icon.setStyleSheet("margin-right:6px")

        timeElapsedWidget=QWidgetAction(self)
        timer = QWidget()
        timer_layout=QHBoxLayout(timer)
        self._timeElapsed=QLabel()

        timer_layout.addWidget(timer_icon)
        timer_layout.addWidget(self._timeElapsed)

        timeElapsedWidget.setDefaultWidget(timer)

        self._timeElapsed.setFont(QFont("Sanserif", 15))

        return timeElapsedWidget

    def updateTimeElapsed(self,sender):
        self._timeElapsed.setText(f"{round(sender.time(),1)}s")


