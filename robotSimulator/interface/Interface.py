from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QActionGroup, QAction, QGridLayout
from PyQt5.uic.properties import QtWidgets

from robotSimulator.Rescaling import Rescaling
from robotSimulator.config import config
from robotSimulator.interface.ExplorerInfo import ExplorerInfo
from robotSimulator.interface.Footer import Footer
from robotSimulator.interface.Header import Header
from robotSimulator.interface.Scene import Scene
from robotSimulator.interface.Explorer import Explorer
from robotSimulator.interface.SceneOverview import SceneOverview
from robotSimulator.interface.ToolsBar import ToolsBar


class Interface(QMainWindow):
    def __init__(self,simulation,environment):
        super().__init__()
        self._simulation = simulation
        self._environment = environment
        self.setWindowTitle("Spicy Simulator")
        self._toolbar=ToolsBar(self._environment,self._simulation,self)


        self._headerWidget=Header()

        self._footer=Footer()
        self._sceneWidget=Scene(self._environment,self._footer)
        self._explorerWidget = Explorer(self._environment, self._footer)
        self._sceneWidget.defineExplorer(self._explorerWidget)


        # TODO : Trouver comment retirer les marges dans les layouts
        self.setMenuBar(self._headerWidget)

        miniSceneWindow = QWidget()
        layout = QVBoxLayout()
        miniSceneWindow.setLayout(layout)
        miniscene = SceneOverview(self._environment)

        layout.addWidget(miniscene)
        miniSceneWindow.setStyleSheet("background-color: #f9f9f9; border: 2px solid #F9886A; border-radius: 8px")
        miniSceneWindow.setFixedSize(250,150) # TODO : Ajuster à la taille de la scène (ex 20 fois plus petit pour garder le ratio)
        Rescaling.miniSceneSize = miniSceneWindow.size()

        centralWidget = QWidget()
        gridLayout = QGridLayout(centralWidget)
        gridLayout.addWidget(self._sceneWidget,0,0)
        gridLayout.addWidget(self._explorerWidget,0,1)
        gridLayout.addWidget(miniSceneWindow,0,0,Qt.AlignRight | Qt.AlignBottom)

        self.setCentralWidget(centralWidget)
        self.setStatusBar(self._footer)

        self.showMaximized()
        self._sceneWidget.maximized()

    def closeEvent(self, event):
        self._simulation.setAppShown(False)
