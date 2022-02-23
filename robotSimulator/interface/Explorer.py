from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QStandardItemModel, QFont, QStandardItem, QIcon
from PyQt5.QtWidgets import QTreeView

from robotSimulator.config import config
from ..Object import Object

from ..robots.Robot import Robot
from ..Obstacle import Obstacle
from ..sensors.Sensor import Sensor
from ..actuators.Actuator import Actuator


class Explorer(QTreeView):

    ITEM_COLOR = "#63656D"
    CRAWLER_COLOR = "#DFE0E5"
    BORDER_COLOR = "#25CCF7"


    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self._mainItems=[]
        self._allItems=[]
        self._mainItemsObjectsAssociated=[]
        self._mainItemsAssociatedChildren = []
        self.treeView()

    def printObjects(self):
        text=""
        for obj in self._environment.getObjects():
            element = type(obj).__name__
            if element != "Object":
                text+=element+"\n"
        return text


    def treeView(self):

        self.setStyleSheet("background-color: #21212F")
        self.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        for obj in self._environment.getObjects():
            if type(obj) != Object:
                parent = Item(obj.getID(), 12, setBold=True)
                # TODO utiliser instanceof
                if isinstance(obj,Robot):
                    parent.setIcon(QIcon(f"{config['ressourcesPath']}/robot.svg"))
                if isinstance(obj,Obstacle):
                    parent.setIcon(QIcon(f"{config['ressourcesPath']}/obstacle.svg"))
                self._mainItems.append(parent)
                self._mainItemsObjectsAssociated.append(obj)
                rootNode.appendRow(parent)
                self._mainItemsAssociatedChildren.append([])
                if hasattr(obj,"getComponents"):
                    for comp in obj.getComponents():
                        child = Item(comp.getID())
                        self._allItems.append(child)
                        self._mainItemsAssociatedChildren[-1].append(child)
                        if isinstance(comp,Actuator):
                            child.setIcon(QIcon(f"{config['ressourcesPath']}/actuator.svg"))
                        if isinstance(comp,Sensor):
                            child.setIcon(QIcon(f"{config['ressourcesPath']}/sensor.svg"))

                        parent.appendRow(child)
        self._allItems.extend(self._mainItems)
        self.setModel(treeModel)
        #self.expandAll()

    def selectionChanged(self, selected, deselected):
        if self.selectedIndexes():
            for obj in self._environment.getObjects():
                obj.setSelected(False)
            for item in self._allItems:
                item.setColor(self.ITEM_COLOR)
            index = self.selectedIndexes()[0]
            crawler = index.model().itemFromIndex(index)
            crawler.setColor(self.CRAWLER_COLOR)
            #self.collapseAll()
            if crawler in self._mainItems:
                selected_obj = self._mainItemsObjectsAssociated[self._mainItems.index(crawler)]
                self.expand(index)
            else:
                selected_obj = self._mainItemsObjectsAssociated[[i for i in range(len(self._mainItems)) if crawler in self._mainItemsAssociatedChildren[i]][0]]
            selected_obj.setSelected(True)

    def setSelectedItem(self,obj):
        self.clearSelection()
        for item in self._allItems:
            item.setColor(self.ITEM_COLOR)
        if obj is not None:
            crawler=self._mainItems[self._mainItemsObjectsAssociated.index(obj)]
            self.expand(crawler.index())
            self.setCurrentIndex(crawler.index())
            crawler.setColor(self.CRAWLER_COLOR)

class Item(QStandardItem):

    def __init__(self, txt='', fontSize=12, setBold=False, color="#63656D"):
        super().__init__()
        fnt = QFont('Verdana', fontSize) # TODO : Changer la font family
        fnt.setBold(setBold)
        self.setEditable(False)
        self.setColor(color)
        self.setFont(fnt)
        self.setText(txt)

    def setColor(self,color):
        self.setForeground(QColor(color))






