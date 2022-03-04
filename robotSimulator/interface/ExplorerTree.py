from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget

from robotSimulator.config import config
from .Button import VisibilityButton
from ..Object import Object
from ..robots.Robot import Robot
from ..Obstacle import Obstacle
from ..sensors.Sensor import Sensor
from ..actuators.Actuator import Actuator

class ExplorerTree(QTreeWidget):

    ITEM_COLOR = "#63656D"
    CRAWLER_COLOR = "#DFE0E5"
    BORDER_COLOR = "#25CCF7"

    # TODO : Revoir la structure du code

    def __init__(self,environment,parent):
        super().__init__()
        self._environment = environment
        self._mainItems=[]
        self._subItems=[]
        self._allObjects = []
        self._mainObjects=[]
        self._childrenButtons=[]
        self._mainItemsAssociatedChildren=[]
        self._visibilityButtons=[]
        self._lockButtons = []

        self._parent=parent

        self._selectedItem=None

        self.treeView()


    def treeView(self):
        self.setHeaderHidden(True)
        self.setColumnCount(2)
        self.setColumnWidth(0,300)
        self.setAutoScroll(True)

        for obj in self._environment.getObjects():
             if type(obj) != Object:
                parent = Item(self,obj.getID(), 12, setBold=True)
                self._visibilityButtons.append(VisibilityButton())
                self.setItemWidget(parent, 1, self._visibilityButtons[-1])
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
                        self._subItems.append(child)
                        self._mainItemsAssociatedChildren[-1].append(child)
                        self._childrenButtons[-1].append(self._visibilityButtons[-1])
                        self._allObjects.append(comp)
                        parent.addChild(child)
                        if isinstance(comp,Actuator):
                            child.setIcon(0,QIcon(f"{config['ressourcesPath']}/actuator.svg"))
                        if isinstance(comp,Sensor):
                            child.setIcon(0,QIcon(f"{config['ressourcesPath']}/sensor.svg"))

        for button in self._visibilityButtons:
            button.clicked.connect(self.toggleObjectVisibily)

        self.resizeColumnToContents(1)

        self.itemClicked.connect(self.clickedItem)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


    def getSelectedObject(self):
        return self._mainObjects[self._mainItems.index(self._selectedItem)] if self._selectedItem is not None else None

    def clickedItem(self):
        crawler = self.currentItem()
        if self._selectedItem is not None:
            self._mainObjects[self._mainItems.index(self._selectedItem)].setSelected(False)
        if crawler in self._mainItems:
            selectedObject = self._mainObjects[self._mainItems.index(crawler)]
        else:
            selectedObject = self._mainObjects[[i for i in range(len(self._mainItems)) if crawler in self._mainItemsAssociatedChildren[i]][0]]
            crawler.setColor(self.CRAWLER_COLOR)
        selectedObject.setSelected(True)

    def setSelectedItem(self,item):
        item.setColor(self.CRAWLER_COLOR)
        item.setExpanded(True)
        self.setCurrentItem(item)
        self._selectedItem=item
        self._parent.showExplorerInfo(self.getSelectedObject())

    def removeSelectedItem(self):
        if self._selectedItem is not None:
            self.clearSelection()
            self._selectedItem.setColor(self.ITEM_COLOR)

            for subItem in self._subItems:
                subItem.setColor(self.ITEM_COLOR)

            self._parent.hideExplorerInfo(self.getSelectedObject())
            self._selectedItem=None

    def refreshView(self,sender):
        crawler = self._mainItems[self._mainObjects.index(sender)]
        if sender.isSelected():
            self.setSelectedItem(crawler)
            # print("add",sender)
        else:
            self.removeSelectedItem()
            # print("remove", sender)

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
                if isinstance(obj,Robot):
                    obj.hideTrajectory()
                for children_button in children_buttons:
                    children_button.lock()
        button.setVisibleObject(obj.isVisible())

class Item(QTreeWidgetItem):

    def __init__(self,parent, txt='', fontSize=12, setBold=False, color="#63656D"):
        super().__init__(parent)
        fnt = QFont("lucida", fontSize) # TODO : Changer la font family
        fnt.setBold(setBold)
        self.setColor(color)
        self.setFont(0,fnt)
        self.setText(0,txt)

    def setColor(self,color):
        self.setForeground(0,QColor(color))


