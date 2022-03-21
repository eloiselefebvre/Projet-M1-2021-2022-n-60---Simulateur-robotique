from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout

from discoverySimulator.ZoomController import ZoomController
from discoverySimulator.config import config
from discoverySimulator.interface.views.Footer import Footer
from discoverySimulator.interface.views.Scene import Scene
from discoverySimulator.interface.views.Explorer import Explorer
from discoverySimulator.interface.views.SceneOverview import SceneOverview
from discoverySimulator.interface.views.Toolbar import Toolbar
from discoverySimulator.robots import Robot

class Interface(QMainWindow):
    def __init__(self,simulation,environment):
        super().__init__()
        self._simulation = simulation
        self._environment = environment
        self.setWindowTitle("Discovery Simulator")

        # self._toolbar=ToolsBar(self._environment,self)
        self._toolbar = Toolbar()

        general_widget=QWidget()
        general_layout=QGridLayout(general_widget)

        zoomController = ZoomController(self._environment)

        self._sceneWidget=Scene(self._environment,zoomController)
        self._explorerWidget = Explorer(self._environment)
        self._footer = Footer(zoomController)

        miniSceneWindow = QWidget()
        layout = QVBoxLayout(miniSceneWindow)
        miniscene = SceneOverview(self._environment,zoomController)

        layout.addWidget(miniscene)
        miniSceneWindow.setStyleSheet("background-color: #f9f9f9; border: 2px solid #F9886A; border-radius: 8px;")
        miniSceneWindow.setFixedSize(250,150) # TODO : Ajuster à la taille de la scène (ex 20 fois plus petit pour garder le ratio)
        zoomController.setMiniSceneSize(miniSceneWindow.size())
        zoomController.zoomToMiniFit()

        general_layout.addWidget(self._toolbar,0,0,1,2)
        general_layout.addWidget(self._sceneWidget,1,0)
        general_layout.addWidget(miniSceneWindow, 1, 0, Qt.AlignRight | Qt.AlignBottom)
        general_layout.addWidget(self._explorerWidget,1,1)
        general_layout.addWidget(self._footer,2,0,1,2)

        general_layout.setContentsMargins(0, 0, 0, 0)
        general_layout.setSpacing(0)

        self.setCentralWidget(general_widget)

        self.showMaximized()
        self._sceneWidget.maximized()

        self._sceneWidget.addObserverCallback(self._footer.updateMousePoseFromScene,"poseChanged")
        zoomController.addObserverCallback(self._footer.updateZoom,"zoomChanged")

        self._simulation.addObserverCallback(self._toolbar.updateTimeElapsed,"timeChanged")

        self._toolbar.addObserverCallback(self._simulation.updateAcceleration,"accelerationChanged")
        self._toolbar.addObserverCallback(self._simulation.updatePlayState, "playChanged")

        self._explorerWidget.getExplorerToolsbar().addObserverCallback(self._sceneWidget.updateLockedScene,"lockChanged")
        self._explorerWidget.getExplorerToolsbar().addObserverCallback(self._explorerWidget.getExplorerTree().rebuildTree,'filterChanged')

        for obj in self._environment.getObjects():
            obj.addObserverCallback(self._explorerWidget.getExplorerTree().changeTreeSelection, "selectionChanged")
            obj.addObserverCallback(self._explorerWidget.getExplorerTree().changeTreeVisibility, "visibilityChanged")
            if hasattr(obj, "getComponents"):
                for comp in obj.getComponents():
                    comp.addObserverCallback(self._explorerWidget.getExplorerTree().changeTreeVisibility,"visibilityChanged")
            self._toolbar.addObserverCallback(obj.accelerationChanged, "accelerationChanged")
            if isinstance(obj,Robot):
                obj.addObserverCallback(self._toolbar.robotSelected,'selectionChanged')
                self._toolbar.addObserverCallback(self._sceneWidget.followPathSelected,'followPathSelected')

    def closeEvent(self, event):
        self._simulation.setAppShown(False)
