from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QStandardItemModel, QFont, QStandardItem, QIcon
from PyQt5.QtWidgets import QTreeView

from robotSimulator.representation.shapes import Border


class Explorer(QTreeView):

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
            element = type(obj).__name__
            if element != "Object":
                parent = Item(element, 12, setBold=True)
                # TODO utiliser instanceof
                if element in ["TwoWheelsRobot","FourWheelsRobot"]:
                    parent.setIcon(QIcon("robotSimulator/ressources/icons/robot.svg"))
                if element == "Obstacle":
                    parent.setIcon(QIcon("robotSimulator/ressources/icons/obstacle.svg"))
                self._mainItems.append(parent)
                self._mainItemsObjectsAssociated.append(obj)
                rootNode.appendRow(parent)
                self._mainItemsAssociatedChildren.append([])
                if hasattr(obj,"getComponents"):
                    for comp in obj.getComponents():
                        subElement = type(comp).__name__
                        child = Item(subElement)
                        self._allItems.append(child)
                        self._mainItemsAssociatedChildren[-1].append(child)
                        if subElement in ["Wheel","LED","Buzzer","Actuator"]:
                            # TODO MSO : mettre dans la config
                            child.setIcon(QIcon("robotSimulator/ressources/icons/actuator.svg"))
                        if subElement in ["Telemeter","LIDAR","Sensor"]:
                            child.setIcon(QIcon("robotSimulator/ressources/icons/sensor.svg"))

                        parent.appendRow(child)
        self._allItems.extend(self._mainItems)
        self.setModel(treeModel)
        #self.expandAll()

    def selectionChanged(self, selected, deselected):
        if self.selectedIndexes():
            for obj in self._mainItemsObjectsAssociated:
                obj.getRepresentation().getShape().removeBorder()
            for item in self._allItems:
                item.setColor("#63656D")
            index = self.selectedIndexes()[0]
            crawler = index.model().itemFromIndex(index)
            crawler.setColor("#DFE0E5")
            if crawler in self._mainItems:
                selected_obj = self._mainItemsObjectsAssociated[self._mainItems.index(crawler)]
            else:
                selected_obj = self._mainItemsObjectsAssociated[[i for i in range(len(self._mainItems)) if crawler in self._mainItemsAssociatedChildren[i]][0]]
            selected_obj.getRepresentation().getShape().addBorder(Border(4,'#25CCF7'))


class Item(QStandardItem):
    def __init__(self, txt='', fontSize=12, setBold=False, color="#63656D"):
        super().__init__()
        fnt = QFont('Times',fontSize) # TODO : Changer la font family
        fnt.setBold(setBold)
        self.setEditable(False)
        self.setColor(color)
        self.setFont(fnt)
        self.setText(txt)

    def setColor(self,color):
        self.setForeground(QColor(color))






