from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import Qt

from robotSimulator.interface.ExplorerFilter import ExplorerFilter
from robotSimulator.interface.ExplorerInfo import ExplorerInfo
from robotSimulator.interface.ExplorerTree import ExplorerTree

class Explorer(QWidget):

    def __init__(self,environment):
        super().__init__()
        self._environment=environment
        self._layout=QGridLayout(self)
        self.setFixedWidth(350)

        self._explorerFilter = ExplorerFilter(self._environment)
        self.setAttribute(Qt.WA_StyledBackground)

        self.setStyleSheet("background-color: #151825")
        self._layout.addWidget(self._explorerFilter,0,0)

        self._explorerInfo=None
        self._showExplorerInfo = False

        self._explorerTree=ExplorerTree(self._environment,self)
        self._layout.addWidget(self._explorerTree,1,0)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)

    def showExplorerInfo(self,obj):
        if not self._showExplorerInfo:
            self._explorerInfo = ExplorerInfo(obj)
            obj.addObserverCallback(self._explorerInfo.refreshData,"poseChanged")
            self._layout.addWidget(self._explorerInfo,2,0)
            self._showExplorerInfo=True

    def hideExplorerInfo(self,obj):
        if self._showExplorerInfo:
            self._layout.removeWidget(self._explorerInfo)
            obj.deleteObserverCallback(self._explorerInfo.refreshData,"poseChanged")
            self._explorerInfo=None
            self._layout.update()
            self._showExplorerInfo=False

    def getExplorerTree(self):
        return self._explorerTree
