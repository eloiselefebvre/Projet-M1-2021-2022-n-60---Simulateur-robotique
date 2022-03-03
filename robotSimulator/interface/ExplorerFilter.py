from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QWidget, QHBoxLayout, QPushButton

from robotSimulator.Obstacle import Obstacle
from robotSimulator.config import config
from robotSimulator.robots.Robot import Robot
from robotSimulator.sensors.Sensor import Sensor


class ExplorerFilter(QWidget):

    def __init__(self,environment):
        super().__init__()
        self._environment=environment
        self._robots = []
        self._sensors = []
        self._obstacles = []
        print(self.robotsFilter())
        print(self.obstaclesFilter())
        print(self.sensorsFilter())

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        self._layout.addWidget(self.menu())
        self._layout.addWidget(self.lock())
        self._layout.addWidget(self.visible())

    def menu(self):
        self._menu = QComboBox()
        self._menu.setFixedWidth(100)
        self._menu.setFixedHeight(30)
        self._menu.setFixedWidth(215)
        self._menu.setStyleSheet("background-color: #f0f0f0")

        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/allObjects.svg"),"All objects")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/robot.svg"),"Robot")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/actuator.svg"),"Actuator")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/sensor.svg"),"Sensor")
        self._menu.addItem(QIcon(f"{config['ressourcesPath']}/obstacle.svg"),"Obstacle")

        return self._menu

    def robotsFilter(self):
        for obj in self._environment.getObjects():
            if isinstance(obj,Robot):
                self._robots.append(obj)
        return self._robots

    def sensorsFilter(self):
        for obj in self._environment.getObjects():
            if isinstance(obj,Sensor):
                self._sensors.append(obj)
        return self._sensors

    def obstaclesFilter(self):
        for obj in self._environment.getObjects():
            if isinstance(obj, Obstacle):
                self._obstacles.append(obj)
        return self._obstacles

    def visible(self):
        self._visibleButton=VisibilityButton()
        self._visibleButton.clicked.connect(self.clickedVisibilityButton)
        return self._visibleButton

    def lock(self):
        self._lockButton=LockButton()
        self._lockButton.clicked.connect(self.clickedLockUnlock)
        return self._lockButton

    def clickedLockUnlock(self):
        for obj in self._environment.getObjects():
            if obj.isLock():
                icon = QIcon(f"{config['ressourcesPath']}/unlock.svg")
                obj.setLock(False)
            else:
                icon = QIcon(f"{config['ressourcesPath']}/lock.svg")
                obj.setLock(True)
            self._lockButton.setIcon(icon)

    def clickedVisibilityButton(self):
        for obj in self._environment.getObjects():
            if obj.isVisible():
                icon = QIcon(f"{config['ressourcesPath']}/invisible.svg")
                obj.setVisible(False)
            else:
                icon = QIcon(f"{config['ressourcesPath']}/visible.svg")
                obj.setVisible(True)
            self._visibleButton.setIcon(icon)



class VisibilityButton(QPushButton):

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

    def __init__(self,lockObj=True):
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
