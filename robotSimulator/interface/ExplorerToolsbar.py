from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QComboBox, QWidget, QHBoxLayout, QPushButton

from robotSimulator.Observable import Observable
from robotSimulator.Obstacle import Obstacle
from robotSimulator.actuators import Actuator
from robotSimulator.config import config
from robotSimulator.robots.Robot import Robot
from robotSimulator.sensors.Sensor import Sensor


class ExplorerToolsbar(QWidget, Observable):

    def __init__(self,environment):
        super().__init__()
        self._environment=environment
        self._robots = []
        self._sensors = []
        self._obstacles = []
        self._actuators = []
        self.objectsFilter()

        self._isSceneLocked=False

        self._layout = QHBoxLayout(self)

        self._layout.addWidget(self.menu())
        self._layout.addWidget(self.lock())
        self._layout.addWidget(self.visible())

    def menu(self):
        fnt=QFont("Verdana", 12)
        self._menu = QComboBox()
        self._menu.setFont(fnt)
        self._menu.setFixedSize(215,30)
        self._menu.setStyleSheet("background-color: #f0f0f0; border:none")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/allObjects.svg"),"All objects")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/robot.svg"),"Robots")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/actuator.svg"),"Actuators")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/sensor.svg"),"Sensors")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/obstacle.svg"),"Obstacles")

        return self._menu


    def objectsFilter(self):
        for obj in self._environment.getObjects():
            if isinstance(obj,Robot):
                self._robots.append(obj)
                for comp in obj.getComponents():
                    if isinstance(comp, Actuator):
                        self._actuators.append(comp)
                    if isinstance(comp, Sensor):
                        self._sensors.append(comp)
            if isinstance(obj, Obstacle):
                self._obstacles.append(obj)

    def visible(self):
        self._visibleButton=VisibilityButton()
        self._visibleButton.clicked.connect(self.clickedVisibilityButton)
        return self._visibleButton

    def lock(self):
        self._lockButton=LockButton()
        self._lockButton.clicked.connect(self.clickedLockUnlock)
        return self._lockButton

    def clickedLockUnlock(self):
        self.toggleSceneLock()
        self._lockButton.setLock(self._isSceneLocked)

    def toggleSceneLock(self):
        self._isSceneLocked=not self._isSceneLocked
        self.notifyObservers("lockChanged")

    def getLockState(self):
        return self._isSceneLocked

    def clickedVisibilityButton(self):
        listObjects=[]
        if self._menu.currentText()=="All objects":
            listObjects=self._environment.getObjects()
        elif self._menu.currentText()=="Robots":
            listObjects=self._robots
        elif self._menu.currentText()=="Sensors":
            listObjects=self._sensors
        elif self._menu.currentText() == "Actuators":
            listObjects = self._actuators
        elif self._menu.currentText()=="Obstacles":
            listObjects=self._obstacles
        for obj in listObjects:
            if obj.isVisible():
                icon = QIcon(f"{config['ressourcesPath']}/invisible.svg")
                obj.setVisible(False)
            else:
                icon = QIcon(f"{config['ressourcesPath']}/visible.svg")
                obj.setVisible(True)
            self._visibleButton.setIcon(icon)


class VisibilityButton(QPushButton): # TODO : Faire une classe Button pour regrouper tous les codes

    def __init__(self,visibleObj=True):
        super().__init__()
        self.setFlat(True)
        self._visibleObj=visibleObj
        self.setVisibleIcon()
        self.setFixedWidth(28)

    def setVisibleIcon(self):
        if self._visibleObj:
            self.setIcon(QIcon(f"{config['ressourcesPath']}/visible.svg"))
        else:
            self.setIcon(QIcon(f"{config['ressourcesPath']}/invisible.svg"))

    def setVisibleObject(self,visibleObj):
        self._visibleObj=visibleObj
        self.setVisibleIcon()

class LockButton(QPushButton):

    def __init__(self,lockObj=False):
        super().__init__()
        self.setFlat(True)
        self._lockObj = lockObj
        self.setLockIcon()
        self.setFixedWidth(28)

    def setLockIcon(self):
        if self._lockObj:
            self.setIcon(QIcon(f"{config['ressourcesPath']}/lock.svg"))
        else:
            self.setIcon(QIcon(f"{config['ressourcesPath']}/unlock.svg"))

    def setLock(self,lock):
        self._lockObj=lock
        self.setLockIcon()
