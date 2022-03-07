from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QComboBox, QWidget, QHBoxLayout

from robotSimulator.config import config

from robotSimulator.Observable import Observable

from robotSimulator.Obstacle import Obstacle
from robotSimulator.actuators import Actuator
from robotSimulator.robots.Robot import Robot
from robotSimulator.sensors.Sensor import Sensor

from robotSimulator.interface.componants.Button import VisibilityButton, LockButton

class ExplorerToolsbar(QWidget, Observable):

    ITEMS = [Robot,Actuator,Sensor,Obstacle]

    # TODO : Mettre tooltip et curseur main sur bouton

    def __init__(self,environment):
        super().__init__()
        self._environment=environment
        self._robots = []
        self._sensors = []
        self._obstacles = []
        self._actuators = []

        self._itemsShown=self.ITEMS

        self._isSceneLocked=False
        self._areObjectVisible=True

        self._filterWidget=self.createFilterWidget()
        self._lockButtonWidget=self.createLockButtonWidget()
        self._visibleButtonWidget=self.createVisibleButtonWidget()

        self._layout = QHBoxLayout(self)
        self._layout.addWidget(self._filterWidget)
        self._layout.addWidget(self._lockButtonWidget)
        self._layout.addWidget(self._visibleButtonWidget)


    # Widgets
    def createFilterWidget(self):
        fnt=QFont("Verdana", 12)
        filterWidget = QComboBox()
        filterWidget.setFont(fnt)
        filterWidget.setFixedSize(215,30)
        filterWidget.setStyleSheet("background-color: #f0f0f0; border:none")
        filterWidget.addItem(QIcon(f"{config['ressourcesPath']}/allObjects.svg"),"All objects")
        for item in self.ITEMS:
            classname=item.__name__
            filterWidget.addItem(QIcon(f"{config['ressourcesPath']}/{classname.lower()}.svg"),classname+"s")

        filterWidget.currentIndexChanged.connect(self.__filterChanged)
        return filterWidget

    def createLockButtonWidget(self):
        lockButton=LockButton()
        lockButton.clicked.connect(self.__clickedLockUnlock)
        return lockButton

    def createVisibleButtonWidget(self):
        visibleButtonWidget = VisibilityButton(self._areObjectVisible)
        visibleButtonWidget.clicked.connect(self.__clickedVisibilityButton)
        return visibleButtonWidget

    def getShownObjects(self):
        objects=[]
        for object in self._environment.getObjects():
            if issubclass(type(object),tuple(self._itemsShown)):
                objects.append(object)
            if isinstance(object, Robot):
                for comp in object.getComponents():
                    if issubclass(type(comp), tuple(self._itemsShown)):
                        objects.append(comp)
        return objects

    def getShownObjectClass(self):
        return self._itemsShown

    # Filter methods
    def __filterChanged(self):
        idx = self._filterWidget.currentIndex()
        if idx!=0:
            self._itemsShown =[]
            self._itemsShown.append(self.ITEMS[idx-1])
        else:
            self._itemsShown = self.ITEMS
        self.setObjectVisible(True)
        self.notifyObservers("filterChanged")

    # Lock methods
    def __clickedLockUnlock(self):
        self.__toggleSceneLock()
        self._lockButtonWidget.setLock(self._isSceneLocked)

    def __toggleSceneLock(self):
        self._isSceneLocked=not self._isSceneLocked
        self.notifyObservers("lockChanged")

    def getLockState(self):
        return self._isSceneLocked

    # Visibility methods
    def __clickedVisibilityButton(self):
        objects=self.getShownObjects()
        self.toggleObjectVisible()
        for object in objects:
            object.setVisible(self._areObjectVisible)
        # TODO : Modifier avec Observer


    def toggleObjectVisible(self):
        self.setObjectVisible(not self._areObjectVisible)

    def setObjectVisible(self,state):
        self._areObjectVisible=state
        self._visibleButtonWidget.setVisibleObject(self._areObjectVisible)