from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QStandardItemModel, QFont, QStandardItem, QIcon
from PyQt5.QtWidgets import QTreeView

from robotSimulator.representation.shapes import Border


class Explorer(QTreeView):

    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self._mainItems=[]
        self._mainItemsObjectsAssociated= []
        self.treeView()

    def printObjects(self):
        text=""
        for obj in self._environment.getObjects():
            element = type(obj).__name__
            if element != "Object":
                text+=element+"\n"
        return text


    def treeView(self):

        self.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        for obj in self._environment.getObjects():
            element = type(obj).__name__
            if element != "Object":
                parent = Item(element, 16, setBold=True)
                if element in ["TwoWheelsRobot","FourWheelsRobot"]:
                    parent.setIcon(QIcon("robotSimulator/ressources/icons/robot.png"))
                if element == "Obstacle":
                    parent.setIcon(QIcon("robotSimulator/ressources/icons/obstacle.png"))
                self._mainItems.append(parent)
                self._mainItemsObjectsAssociated.append(obj)
                rootNode.appendRow(parent)
                if hasattr(obj,"getComponents"):
                    for comp in obj.getComponents():
                        subElement = type(comp).__name__
                        child = Item(subElement)
                        if subElement in ["Wheel","LED","Buzzer","Actuator"]:
                            child.setIcon(QIcon("robotSimulator/ressources/icons/actuator.png"))
                        if subElement in ["Telemeter","LIDAR","Sensor"]:
                            child.setIcon(QIcon("robotSimulator/ressources/icons/sensor.png"))



                        parent.appendRow(child)

        self.setModel(treeModel)
        self.expandAll()

    def selectionChanged(self, selected, deselected):
        if self.selectedIndexes():
            for obj in self._mainItemsObjectsAssociated:
                obj.getRepresentation().getShape().removeBorder()
            index = self.selectedIndexes()[0]
            crawler = index.model().itemFromIndex(index)
            if crawler in self._mainItems:
                selected_obj = self._mainItemsObjectsAssociated[self._mainItems.index(crawler)]
                selected_obj.getRepresentation().getShape().addBorder(Border(4,'#25CCF7'))



class Item(QStandardItem):
    def __init__(self, txt='', fontSize=12, setBold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', fontSize)
        fnt.setBold(setBold)
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)






