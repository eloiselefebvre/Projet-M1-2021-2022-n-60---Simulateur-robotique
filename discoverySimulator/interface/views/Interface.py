from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout
from discoverySimulator.ZoomController import ZoomController
from discoverySimulator.config import colors
from discoverySimulator.interface.views.Footer import Footer
from discoverySimulator.interface.views.Scene import Scene
from discoverySimulator.interface.views.Explorer import Explorer
from discoverySimulator.interface.views.SceneOverview import SceneOverview
from discoverySimulator.interface.views.Toolbar import Toolbar
from discoverySimulator.robots import Robot

class Interface(QMainWindow):
    def __init__(self,simulation,environment):
        super().__init__()
        self.__simulation = simulation
        self.__environment = environment
        self.setWindowTitle("Discovery Simulator")
        self.__toolbar = Toolbar()
        general_widget=QWidget()
        general_layout=QGridLayout(general_widget)
        zoomController = ZoomController(self.__environment)
        self.__sceneWidget=Scene(self.__environment, zoomController)
        self.__explorerWidget = Explorer(self.__environment)
        self.__footer = Footer(zoomController)
        miniSceneWindow = QWidget()
        layout = QVBoxLayout(miniSceneWindow)
        miniscene = SceneOverview(self.__environment, zoomController)
        layout.addWidget(miniscene)
        miniSceneWindow.setStyleSheet(f"background-color: {colors['font']} ; border: 2px solid "+colors['sceneOverviewBorder']+"; border-radius: 8px;")
        miniSceneWindow.setFixedSize(320,180) # ratio 16:9
        zoomController.setMiniSceneSize(miniSceneWindow.size())
        zoomController.zoomToMiniFit()

        general_layout.addWidget(self.__toolbar, 0, 0, 1, 2)
        general_layout.addWidget(self.__sceneWidget, 1, 0)
        general_layout.addWidget(miniSceneWindow, 1, 0, Qt.AlignRight | Qt.AlignBottom)
        general_layout.addWidget(self.__explorerWidget, 1, 1)
        general_layout.addWidget(self.__footer, 2, 0, 1, 2)

        general_layout.setContentsMargins(0, 0, 0, 0)
        general_layout.setSpacing(0)

        self.setCentralWidget(general_widget)

        self.showMaximized()
        self.__sceneWidget.maximized()

        self.__sceneWidget.addObserverCallback(self.__footer.updateMousePoseFromScene, "poseChanged")
        zoomController.addObserverCallback(self.__footer.updateZoom, "zoomChanged")

        self.__simulation.addObserverCallback(self.__toolbar.updateTimeElapsed, "timeChanged")

        self.__toolbar.addObserverCallback(self.__simulation.updateAcceleration, "accelerationChanged")
        self.__toolbar.addObserverCallback(self.__simulation.updatePlayState, "playChanged")

        self.__explorerWidget.getExplorerToolsbar().addObserverCallback(self.__sceneWidget.updateLockedScene, "lockChanged")
        self.__explorerWidget.getExplorerToolsbar().addObserverCallback(self.__explorerWidget.getExplorerTree().rebuildTree, 'filterChanged')

        for obj in self.__environment.getObjects():
            obj.addObserverCallback(self.__explorerWidget.getExplorerTree().changeTreeSelection, "selectionChanged")
            obj.addObserverCallback(self.__explorerWidget.getExplorerTree().changeTreeVisibility, "visibilityChanged")
            if hasattr(obj, "getComponents"):
                for comp in obj.getComponents():
                    comp.addObserverCallback(self.__explorerWidget.getExplorerTree().changeTreeVisibility, "visibilityChanged")
            self.__toolbar.addObserverCallback(obj.accelerationChanged, "accelerationChanged")
            if isinstance(obj,Robot):
                obj.addObserverCallback(self.__toolbar.robotSelected, 'selectionChanged')
        self.__toolbar.addObserverCallback(self.__sceneWidget.followPathSelected, 'followPathSelected')

    def closeEvent(self, event):
        self.__simulation.setAppShown(False)
