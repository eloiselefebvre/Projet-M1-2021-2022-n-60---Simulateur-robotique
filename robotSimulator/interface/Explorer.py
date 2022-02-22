from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QStandardItemModel, QFont, QStandardItem
from PyQt5.QtWidgets import QTreeView

from robotSimulator.representation.shapes import Border


class Explorer(QTreeView):

    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self._mainItems=[]
        self._mainItemsObjectsAssociated= []
        self.treeView()

    def treeView(self):
        self.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        for obj in self._environment.getObjects():
            element = type(obj).__name__
            if element != "Object":
                parent = Item(element, 16, setBold=True)
                self._mainItems.append(parent)
                self._mainItemsObjectsAssociated.append(obj)
                rootNode.appendRow(parent)
                if hasattr(obj,"getComponents"):
                    for comp in obj.getComponents():
                        parent.appendRow(Item(type(comp).__name__))

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






