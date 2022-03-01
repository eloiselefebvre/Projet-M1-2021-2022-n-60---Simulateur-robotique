from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget, QLayout

from robotSimulator.config import config
from .Scene import Scene
from .ExplorerInfo import ExplorerInfo
from .SceneOverview import SceneOverview
from ..Object import Object
from ..Rescaling import Rescaling
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QWidget

from robotSimulator.interface.ExplorerInfo import ExplorerInfo
from robotSimulator.interface.ExplorerTree import ExplorerTree

class Explorer(QTreeWidget):

class Explorer(QWidget):

    def __init__(self,environment,footer):
        super().__init__()
        self._environment=environment
        self._footer=footer
        self._layout=QGridLayout(self)

        self._explorerInfo=None
        self._showExplorerInfo = False

        self._explorerTree=ExplorerTree(self._environment,self._footer,self)
        self._layout.addWidget(self._explorerTree,0,0)

    def showExplorerInfo(self,obj):
        if not self._showExplorerInfo:
            self._explorerInfo = ExplorerInfo(obj)
            self._explorerInfo.setStyleSheet("background-color: #21212F")
            self._explorerInfo.setFixedHeight(400)
            self._layout.addWidget(self._explorerInfo,1,0)
            self._showExplorerInfo=True

    def getExplorerTree(self):
        return self._explorerTree

    def hideExplorerInfo(self):
        if self._showExplorerInfo:
            self._layout.removeWidget(self._explorerInfo)
            self._explorerInfo=None
            self._layout.update()
            self._showExplorerInfo=False