from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QActionGroup, QAction
from PyQt5.uic.properties import QtWidgets

from robotSimulator.config import config
from robotSimulator.interface.ExplorerInfo import ExplorerInfo
from robotSimulator.interface.Footer import Footer
from robotSimulator.interface.Header import Header
from robotSimulator.interface.Scene import Scene
from robotSimulator.interface.Explorer import Explorer
from robotSimulator.interface.ToolsBar import ToolsBar


class Interface(QMainWindow):
    def __init__(self,simulation,environment):
        super().__init__()
        self._simulation = simulation
        self._environment = environment
        self.setWindowTitle("Spicy Simulator")
        self._toolbar=ToolsBar(self._environment,self._simulation,self)

        widget=QWidget()
        self._generalLayout = QVBoxLayout()
        widget.setLayout(self._generalLayout)

        self._informationLayout = QHBoxLayout()

        self._headerWidget=Header()

        self._footer=Footer()
        self._explorerWidget=Explorer(self._environment,self._footer)
        self._sceneWidget=Scene(self._environment,self._explorerWidget,self._footer)

        self._generalLayout.addWidget(self._toolbar)
        self._informationLayout.addWidget(self._sceneWidget,90)
        self._informationLayout.addWidget(self._explorerWidget,10)
        self._generalLayout.addLayout(self._informationLayout)

        # TODO : Trouver comment retirer les marges dans les layouts
        self.setMenuBar(self._headerWidget)
        self.setCentralWidget(widget)
        self.setStatusBar(self._footer)

        self.showMaximized()
        self._sceneWidget.maximized()

    def closeEvent(self, event):
        self._simulation.setAppShown(False)
