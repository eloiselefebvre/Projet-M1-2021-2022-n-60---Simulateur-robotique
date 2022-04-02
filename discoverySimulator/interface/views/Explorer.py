from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import Qt

from discoverySimulator.config import colors
from discoverySimulator.interface.views.ExplorerToolbar import ExplorerToolsbar
from discoverySimulator.interface.views.ExplorerInfo import ExplorerInfo
from discoverySimulator.interface.views.ExplorerTree import ExplorerTree

class Explorer(QWidget):

    __EXPLORER_WIDTH = 350

    def __init__(self,environment):
        super().__init__()
        self.setFixedWidth(Explorer.__EXPLORER_WIDTH)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("*{background-color: " + colors['explorerBackground']+ "; border:none}")

        self.__layout=QGridLayout(self)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)

        self.__environment=environment

        self.__explorerToolsbar = ExplorerToolsbar(self.__environment)
        self.__explorerTree=ExplorerTree(self.__environment, self)
        self.__explorerInfo=None

        self.__layout.addWidget(self.__explorerToolsbar, 0, 0)
        self.__layout.addWidget(self.__explorerTree, 1, 0)


    # GETTERS
    def getExplorerTree(self):
        return self.__explorerTree

    def getExplorerToolsbar(self):
        return self.__explorerToolsbar

    def showExplorerInfo(self,obj):
        if self.__explorerInfo is None:
            self.__explorerInfo = ExplorerInfo(self.__environment, obj)
            obj.addObserverCallback(self.__explorerInfo.refreshData, "stateChanged")
            self.__layout.addWidget(self.__explorerInfo, 2, 0)

    def hideExplorerInfo(self,obj):
        if self.__explorerInfo is not None:
            self.__layout.removeWidget(self.__explorerInfo)
            obj.deleteObserverCallback(self.__explorerInfo.refreshData, "stateChanged")
            self.__explorerInfo=None
            self.__layout.update()


