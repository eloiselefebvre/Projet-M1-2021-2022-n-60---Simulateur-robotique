from PyQt5.QtGui import QPalette, QColor, QStandardItemModel, QFont, QStandardItem
from PyQt5.QtWidgets import QWidget, QTreeView




class Explorer(QTreeView):

    def __init__(self,environment):
        super().__init__()
        self._environment = environment
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
                rootNode.appendRow(parent)
                if hasattr(obj,"getComponents"):
                    for comp in obj.getComponents():
                        parent.appendRow(Item(type(comp).__name__))

        self.setModel(treeModel)
        self.expandAll()


class Item(QStandardItem):
    def __init__(self, txt='', fontSize=12, setBold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', fontSize)
        fnt.setBold(setBold)
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)






