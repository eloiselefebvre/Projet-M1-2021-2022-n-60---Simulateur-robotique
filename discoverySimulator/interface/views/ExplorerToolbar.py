from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QComboBox, QWidget, QHBoxLayout
from discoverySimulator.config import config, colors
from discoverySimulator.Observable import Observable
from discoverySimulator.obstacles.Obstacle import Obstacle
from discoverySimulator.actuators import Actuator
from discoverySimulator.robots.Robot import Robot
from discoverySimulator.sensors.Sensor import Sensor
from discoverySimulator.interface.components.Button import VisibilityButton, LockButton

class ExplorerToolsbar(QWidget, Observable):

    __ITEMS = [Robot, Actuator, Sensor, Obstacle]

    def __init__(self,environment):
        super().__init__()
        self.__environment=environment
        self.__robots = []
        self.__sensors = []
        self.__obstacles = []
        self.__actuators = []
        self.__itemsShown=self.__ITEMS
        self.__isSceneLocked=False
        self.__areObjectVisible=True
        self.__filterWidget=self.__createFilterWidget()
        self.__lockButtonWidget=self.__createLockButtonWidget()
        self.__visibleButtonWidget=self.__createVisibleButtonWidget()

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.__filterWidget)
        self.__layout.addWidget(self.__lockButtonWidget)
        self.__layout.addWidget(self.__visibleButtonWidget)

    # GETTERS
    def getShownObjects(self):
        objects=[]
        for object in self.__environment.getObjects():
            if issubclass(type(object), tuple(self.__itemsShown)):
                objects.append(object)
            if isinstance(object, Robot):
                for comp in object.getComponents():
                    if issubclass(type(comp), tuple(self.__itemsShown)):
                        objects.append(comp)
        return objects

    def getShownObjectClass(self):
        return self.__itemsShown

    # Widgets
    def __createFilterWidget(self) -> QComboBox:
        fnt=QFont("Verdana", 12)
        filterWidget = QComboBox()
        filterWidget.setFont(fnt)
        filterWidget.setFixedSize(215,30)
        filterWidget.setStyleSheet("background-color:"+colors['font']+"; border:none")
        filterWidget.addItem(QIcon(f"{config['ressourcesPath']}/objects/allObjects.svg"),"All objects")
        for item in self.__ITEMS:
            classname=item.__name__
            filterWidget.addItem(QIcon(f"{config['ressourcesPath']}/objects/{classname.lower()}.svg"),classname+"s")
        filterWidget.currentIndexChanged.connect(self.__filterChanged)
        return filterWidget

    def __createLockButtonWidget(self) -> LockButton:
        lockButton=LockButton()
        lockButton.clicked.connect(self.__clickedLockUnlock)
        lockButton.setToolTip("Unlock" if self.__isSceneLocked else "Lock")
        return lockButton

    def __createVisibleButtonWidget(self) -> VisibilityButton:
        visibleButtonWidget = VisibilityButton(self.__areObjectVisible)
        visibleButtonWidget.clicked.connect(self.__clickedVisibilityButton)
        visibleButtonWidget.setToolTip("Hide" if self.__areObjectVisible else "Show")
        return visibleButtonWidget

    # Filter methods
    def __filterChanged(self):
        idx = self.__filterWidget.currentIndex()
        if idx!=0:
            self.__itemsShown =[]
            self.__itemsShown.append(self.__ITEMS[idx - 1])
        else:
            self.__itemsShown = self.__ITEMS
        self.setObjectVisible(True)
        self.notifyObservers("filterChanged")

    # Lock methods
    def __clickedLockUnlock(self):
        self.__toggleSceneLock()
        self.__lockButtonWidget.setToolTip("Unlock" if self.__isSceneLocked else "Lock")
        self.__lockButtonWidget.setState(self.__isSceneLocked)

    def __toggleSceneLock(self):
        self.__isSceneLocked=not self.__isSceneLocked
        self.notifyObservers("lockChanged")

    def getLockState(self) -> bool:
        return self.__isSceneLocked

    # Visibility methods
    def __clickedVisibilityButton(self):
        objects=self.getShownObjects()
        self.toggleObjectVisible()
        self.__visibleButtonWidget.setToolTip("Hide" if self.__areObjectVisible else "Show")
        for object in objects:
            object.setVisible(self.__areObjectVisible)

    def toggleObjectVisible(self):
        self.setObjectVisible(not self.__areObjectVisible)

    def setObjectVisible(self,state):
        self.__areObjectVisible=state
        self.__visibleButtonWidget.setState(self.__areObjectVisible)
