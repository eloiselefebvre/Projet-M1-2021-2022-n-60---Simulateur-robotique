from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import Qt

from discoverySimulator.interface.views.ExplorerToolbar import ExplorerToolsbar
from discoverySimulator.interface.views.ExplorerInfo import ExplorerInfo
from discoverySimulator.interface.views.ExplorerTree import ExplorerTree

class Explorer(QWidget):

    def __init__(self,environment):
        super().__init__()
        self._environment=environment
        self._layout=QGridLayout(self)
        self.setFixedWidth(350)

        self._explorerToolsbar = ExplorerToolsbar(self._environment)
        self.setAttribute(Qt.WA_StyledBackground)

        self.setStyleSheet("*{background-color: #151825; border:none}"
                           "QPushButton:hover{background-color:#323247;}"
                           "QPushButton:pressed{background-color:#4C4C68;}")
        self._layout.addWidget(self._explorerToolsbar, 0, 0)

        self._explorerInfo=None

        self._explorerTree=ExplorerTree(self._environment,self)
        self._layout.addWidget(self._explorerTree,1,0)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)

    def showExplorerInfo(self,obj):
        if self._explorerInfo is None:
            self._explorerInfo = ExplorerInfo(self._environment,obj)
            obj.addObserverCallback(self._explorerInfo.refreshData, "stateChanged")
            self._layout.addWidget(self._explorerInfo, 2, 0)

    def hideExplorerInfo(self,obj):
        if self._explorerInfo is not None:
            self._layout.removeWidget(self._explorerInfo)
            obj.deleteObserverCallback(self._explorerInfo.refreshData, "stateChanged")
            self._explorerInfo=None
            self._layout.update()

    def getExplorerTree(self):
        return self._explorerTree

    def getExplorerToolsbar(self):
        return self._explorerToolsbar
