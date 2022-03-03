from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QActionGroup, QAction, QGridLayout

from robotSimulator.ZoomController import ZoomController
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

        self._headerWidget = Header()
        self._toolbar=ToolsBar(self._environment,self)

        zoomController = ZoomController(self._environment)

        self._sceneWidget=Scene(self._environment,zoomController)
        self._explorerWidget = Explorer(self._environment)
        self._sceneWidget.defineExplorer(self._explorerWidget.getExplorerTree()) # TODO : A enlever avec ajout d'overvateurs
        self._footer = Footer(zoomController)

        self.setMenuBar(self._headerWidget)

        miniSceneWindow = QWidget()
        layout = QVBoxLayout()
        miniSceneWindow.setLayout(layout)
        miniscene = SceneOverview(self._environment,zoomController)

        layout.addWidget(miniscene)
        miniSceneWindow.setStyleSheet("background-color: #f9f9f9; border: 2px solid #F9886A; border-radius: 8px")
        miniSceneWindow.setFixedSize(250,150) # TODO : Ajuster à la taille de la scène (ex 20 fois plus petit pour garder le ratio)
        zoomController.setMiniSceneSize(miniSceneWindow.size())
        zoomController.zoomToMiniFit()

        centralWidget = QWidget()
        gridLayout = QGridLayout(centralWidget)
        gridLayout.addWidget(self._sceneWidget,0,0)
        gridLayout.addWidget(self._explorerWidget,0,1)
        gridLayout.addWidget(miniSceneWindow,0,0,Qt.AlignRight | Qt.AlignBottom)

        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setSpacing(0)


        self.setCentralWidget(centralWidget)
        self.setStatusBar(self._footer)

        self.showMaximized()
        self._sceneWidget.maximized()

        for object in self._environment.getObjects():
            object.addObserverCallback(self._explorerWidget.getExplorerTree().refreshView)

        self._simulation.addObserverCallback(self._sceneWidget.refreshView)

        self._sceneWidget.addObserverCallback(self._footer.updateMousePoseFromScene)
        zoomController.addObserverCallback(self._footer.updateZoom)

        self._toolbar.addObserverCallback(self._simulation.updateAcceleration)

    def closeEvent(self, event):
        self._simulation.setAppShown(False)
