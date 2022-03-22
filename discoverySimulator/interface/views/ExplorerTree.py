from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from discoverySimulator.config import config
from discoverySimulator.interface.components.Button import VisibilityButton
from discoverySimulator.Object import Object
from discoverySimulator.robots.Robot import Robot
from discoverySimulator.obstacles.Obstacle import Obstacle
from discoverySimulator.sensors.Sensor import Sensor
from discoverySimulator.actuators.Actuator import Actuator

class ExplorerTree(QTreeWidget):

    ITEM_COLOR = "#63656D"
    CRAWLER_COLOR = "#DFE0E5"
    BORDER_COLOR = "#25CCF7"

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

        self._parent=parent
        self._selectedItem=None
        self._selectedSubItem=None
        self._itemsShown=[Robot,Actuator,Sensor,Obstacle]

        self.setTreeWidgetConfiguration()
        self.buildTree()

    def setTreeWidgetConfiguration(self):
        self.setHeaderHidden(True)
        self.setColumnCount(2)
        self.setColumnWidth(0, 300)
        self.setAutoScroll(True)
        self.resizeColumnToContents(1)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def rebuildTree(self,sender):
        self._itemsShown=sender.getShownObjectClass()
        self.clearTree()
        self.buildTree()
        self.expandAll()

    def clearTree(self):
        if self._selectedItem is not None:
            self._mainObjects[self._mainItems.index(self._selectedItem)].setSelected(False)
        self.removeSelectedItem()
        self.itemClicked.disconnect(self.clickedItem)

        root = self.invisibleRootItem()
        parents = []
        for i in range(root.childCount()):
            parents.append(root.child(i))
            childs = []
            for j in range(parents[-1].childCount()):
                childs.append(parents[-1].child(j))
            for child in childs:
                parents[-1].removeChild(child)
        for parent in parents:
            root.removeChild(parent)

        self._mainItems.clear()
        self._subItems.clear()
        self._allObjects.clear()
        self._mainObjects.clear()
        self._childrenButtons.clear()
        self._mainItemsAssociatedChildren.clear()
        self._visibilityButtons.clear()

    def buildTree(self):
        for obj in self._environment.getObjects():
             if type(obj) != Object:
                if issubclass(type(obj),tuple(self._itemsShown)) or (isinstance(obj,Robot) and (Actuator in self._itemsShown or Sensor in self._itemsShown)):
                    parent=None
                    if not issubclass(type(obj),tuple(self._itemsShown)) and isinstance(obj,Robot) and (Actuator in self._itemsShown or Sensor in self._itemsShown):
                        sensors = [comp  for comp in obj.getComponents() if isinstance(comp,Sensor)]
                        if (Sensor in self._itemsShown and sensors) or (Actuator in self._itemsShown and len(obj.getComponents())-len(sensors)!=0):
                            parent = Item(self, obj.getID(), 12, setBold=True)
                            parent.setIcon(0,QIcon(f"{config['ressourcesPath']}/robotDisabled.svg"))
                            self._visibilityButtons.append(None)
                    else:
                        parent = Item(self, obj.getID(), 12, setBold=True)
                        classname = [item for item in self._itemsShown if isinstance(obj,item)][0].__name__
                        parent.setIcon(0,QIcon(f"{config['ressourcesPath']}/objects/{classname.lower()}.svg"))
                        self._visibilityButtons.append(VisibilityButton(obj.isVisible()))
                        self.setItemWidget(parent, 1, self._visibilityButtons[-1])
                    if parent is not None:
                        self._mainItems.append(parent)
                        self._mainObjects.append(obj)
                        self._allObjects.append(obj)
                        self._mainItemsAssociatedChildren.append([])
                        self._childrenButtons.append([])
                        if hasattr(obj,"getComponents"):
                            for comp in obj.getComponents():
                                if issubclass(type(comp),tuple(self._itemsShown)):
                                    child = Item(parent,comp.getID())
                                    self._visibilityButtons.append(VisibilityButton(comp.isVisible()))
                                    if comp.getVisibilityLocked():
                                        self._visibilityButtons[-1].lock()
                                    self.setItemWidget(child, 1, self._visibilityButtons[-1])
                                    self._subItems.append(child)
                                    self._mainItemsAssociatedChildren[-1].append(child)
                                    self._childrenButtons[-1].append(self._visibilityButtons[-1])
                                    self._allObjects.append(comp)
                                    parent.addChild(child)
                                    classname = [item for item in self._itemsShown if isinstance(comp, item)][0].__name__
                                    child.setIcon(0,QIcon(f"{config['ressourcesPath']}/objects/{classname.lower()}.svg"))
        for button in self._visibilityButtons:
            if button is not None:
                button.clicked.connect(self.toggleObjectVisibily)
        self.itemClicked.connect(self.clickedItem)

    def clickedItem(self):
        crawler = self.currentItem()
        if self._selectedItem is not None:
            self._mainObjects[self._mainItems.index(self._selectedItem)].setSelected(False)
        if crawler in self._mainItems:
            selectedObject = self._mainObjects[self._mainItems.index(crawler)]
        else:
            selectedObject = self._mainObjects[[i for i in range(len(self._mainItems)) if crawler in self._mainItemsAssociatedChildren[i]][0]]
            crawler.setColor(self.CRAWLER_COLOR)
            self._selectedSubItem=crawler
        selectedObject.setSelected(True)

    def setSelectedItem(self,item):
        item.setColor(self.CRAWLER_COLOR)
        item.setExpanded(True)
        self.setCurrentItem(item)
        self._selectedItem=item
        if self._selectedSubItem is not None:
            self._parent.showExplorerInfo(self._allObjects[1+ self._mainItems.index(self._selectedItem) + self._subItems.index(self._selectedSubItem)])
        else:
            self._parent.showExplorerInfo(self._mainObjects[self._mainItems.index(self._selectedItem)])

    def removeSelectedItem(self):
        if self._selectedItem is not None:
            self.clearSelection()
            self._selectedItem.setColor(self.ITEM_COLOR)

            for subItem in self._subItems:
                subItem.setColor(self.ITEM_COLOR)

            if self._selectedSubItem is not None:
                self._parent.hideExplorerInfo(self._allObjects[1 + self._mainItems.index(self._selectedItem) + self._subItems.index(self._selectedSubItem)])
            else:
                self._parent.hideExplorerInfo(self._mainObjects[self._mainItems.index(self._selectedItem)])
            self._selectedItem=None
            self._selectedSubItem=None

    def changeTreeSelection(self,sender):
        if sender in self._mainObjects:
            crawler = self._mainItems[self._mainObjects.index(sender)]
            if sender.isSelected():
                self.setSelectedItem(crawler)
            else:
                self.removeSelectedItem()

    def changeTreeVisibility(self,sender):
        if sender in self._allObjects:
            button=self._visibilityButtons[self._allObjects.index(sender)]
            button.setState(sender.isVisible())
            if sender in self._mainObjects:
                children_buttons = self._childrenButtons[self._mainObjects.index(sender)]
                if sender.isVisible():
                    for children_button in children_buttons:
                        children_button.unlock()
                else:
                    for children_button in children_buttons:
                        children_button.lock()

    def toggleObjectVisibily(self):
        button = self.sender()
        obj = self._allObjects[self._visibilityButtons.index(button)]
        obj.toggleVisible()

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


