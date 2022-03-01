from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget

from robotSimulator.config import config
from .Scene import Scene
from .ExplorerInfo import ExplorerInfo
from ..Object import Object
from ..Rescaling import Rescaling

from ..robots.Robot import Robot
from ..Obstacle import Obstacle
from ..sensors.Sensor import Sensor
from ..actuators.Actuator import Actuator

class Explorer(QTreeWidget):

    ITEM_COLOR = "#63656D"
    CRAWLER_COLOR = "#DFE0E5"
    BORDER_COLOR = "#25CCF7"

    # TODO : Revoir la structure du code

    def __init__(self,environment,footer):
        super().__init__()
        self._environment = environment
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._layout.setSpacing(0)
        self._showExplorerInfo = False
        self._mainItems=[]
        self._allItems=[]
        self._allObjects = []
        self._mainObjects=[]
        self._childrenButtons=[]
        self._mainItemsAssociatedChildren=[]
        self._visibilityButtons=[]
        self._lockButtons = []
        self._footer=footer
        self.treeView()
        self._layout.addWidget(self)
        self._layout.addWidget(self.generalView())

    def generalView(self):
        generalViewWidget=QWidget()
        layout=QVBoxLayout()
        generalViewWidget.setLayout(layout)
        generalView = Scene(self._environment, self, self._footer)
        layout.addWidget(generalView)
        generalViewWidget.setFixedWidth(300)
        generalViewWidget.setFixedHeight(200)
        generalViewWidget.setStyleSheet("background-color:#f0f0f0")
        return generalViewWidget

    def treeView(self):
        self.setFixedWidth(320)
        self.setHeaderHidden(True)
        self.setColumnCount(3)
        self.setColumnWidth(0,240)
        self.setAutoScroll(True)
        self.setStyleSheet("background-color: #151825")

        for obj in self._environment.getObjects():
             if type(obj) != Object:
                parent = Item(self,obj.getID(), 12, setBold=True)
                self._visibilityButtons.append(VisibilityButton())
                self.setItemWidget(parent, 1, self._visibilityButtons[-1])
                self._lockButtons.append(LockButton(obj.isLock()))
                self.setItemWidget(parent, 2, self._lockButtons[-1])
                if isinstance(obj,Robot):
                    parent.setIcon(0,QIcon(f"{config['ressourcesPath']}/robot.svg"))
                if isinstance(obj,Obstacle):
                    parent.setIcon(0,QIcon(f"{config['ressourcesPath']}/obstacle.svg"))
                if isinstance(obj, Sensor):
                    parent.setIcon(0, QIcon(f"{config['ressourcesPath']}/sensor.svg"))
                self._mainItems.append(parent)
                self._mainObjects.append(obj)
                self._allObjects.append(obj)
                self._mainItemsAssociatedChildren.append([])
                self._childrenButtons.append([])
                if hasattr(obj,"getComponents"):
                    for comp in obj.getComponents():
                        child = Item(parent,comp.getID())
                        self._visibilityButtons.append(VisibilityButton())
                        self.setItemWidget(child, 1, self._visibilityButtons[-1])
                        self._allItems.append(child)
                        self._mainItemsAssociatedChildren[-1].append(child)
                        self._childrenButtons[-1].append(self._visibilityButtons[-1])
                        self._allObjects.append(comp)
                        parent.addChild(child)
                        if isinstance(comp,Actuator):
                            child.setIcon(0,QIcon(f"{config['ressourcesPath']}/actuator.svg"))
                        if isinstance(comp,Sensor):
                            child.setIcon(0,QIcon(f"{config['ressourcesPath']}/sensor.svg"))
        self._allItems.extend(self._mainItems)

        for button in self._visibilityButtons:
            button.clicked.connect(self.toggleObjectVisibily)

        for button in self._lockButtons:
            button.clicked.connect(self.toggleObjectLock)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
        #self.expandAll()

    def openWindow(self):
        widget=QWidget()
        self._layout.addWidget(widget,10)
        widget.setStyleSheet("background-color: #f0f0f0")

    def showExplorerInfo(self,obj):
        if not self._showExplorerInfo:
            self._showExplorerInfo=True
            self._explorerInfo = ExplorerInfo(obj)
            self._explorerInfo.setStyleSheet("background-color: #21212F")
            self._explorerInfo.setFixedHeight(400)
            self._layout.addWidget(self._explorerInfo)

    def hideExplorerInfo(self):
        if self._showExplorerInfo:
            self._showExplorerInfo=False
            self._layout.removeWidget(self._explorerInfo)

    def selectionChanged(self, selected, deselected):
        self.hideExplorerInfo()
        if self.selectedIndexes():
            for obj in self._environment.getObjects():
                obj.setSelected(False)
            for item in self._allItems:
                item.setColor(self.ITEM_COLOR)
            crawler = self.currentItem()
            crawler.setColor(self.CRAWLER_COLOR)
            if crawler in self._mainItems:
                selected_obj = self._mainObjects[self._mainItems.index(crawler)]
            else:
                selected_obj = self._mainObjects[[i for i in range(len(self._mainItems)) if crawler in self._mainItemsAssociatedChildren[i]][0]]
            selected_obj.setSelected(True)
            self.showExplorerInfo(selected_obj)

    def setSelectedItem(self,obj):
        self.clearSelection()
        for item in self._allItems:
            item.setColor(self.ITEM_COLOR)
        if obj is not None:
            crawler=self._mainItems[self._mainObjects.index(obj)]
            crawler.setColor(self.CRAWLER_COLOR)
            crawler.setExpanded(True)
            self.setCurrentItem(crawler)

    def toggleObjectVisibily(self):
        button = self.sender()
        obj = self._allObjects[self._visibilityButtons.index(button)]
        obj.toggleVisible()
        if obj in self._mainObjects:
            children_buttons=self._childrenButtons[self._mainObjects.index(obj)]
            if obj.isVisible():
                for children_button in children_buttons:
                    children_button.unlock()
            else:
                for children_button in children_buttons:
                    children_button.lock()
        button.setVisibleObject(obj.isVisible())

    def toggleObjectLock(self):
        button = self.sender()
        obj=self._mainObjects[self._lockButtons.index(button)]
        obj.toggleLock()
        button.setLockObject(obj.isLock())


class Item(QTreeWidgetItem):

    def __init__(self,parent, txt='', fontSize=12, setBold=False, color="#63656D"):
        super().__init__(parent)
        fnt = QFont('Verdana', fontSize) # TODO : Changer la font family
        fnt.setBold(setBold)
        self.setColor(color)
        self.setFont(0,fnt)
        self.setText(0,txt)

    def setColor(self,color):
        self.setForeground(0,QColor(color))

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

    def lock(self):
        self.setDisabled(True)
        self.setIcon(QIcon(f"{config['ressourcesPath']}/point.svg"))

    def unlock(self):
        self.setDisabled(False)
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

    def setLockObject(self, lockObj):
        self._lockObj = lockObj
        self.setLockIcon()