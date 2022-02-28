from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from robotSimulator.interface.ExplorerInfo import ExplorerInfo
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

        widget=QWidget()
        self._generalLayout = QVBoxLayout()
        widget.setLayout(self._generalLayout)

        self._informationLayout = QHBoxLayout()

        self._headerWidget=Header()
        self._toolsBarWidget = ToolsBar(self._environment,self._simulation)
        self._explorerWidget=Explorer(self._environment)
        self._sceneWidget=Scene(self._environment,self._explorerWidget)

        self._informationLayout.addWidget(self._sceneWidget,90)
        self._informationLayout.addWidget(self._explorerWidget,10)

        #ajout des deux layout du QVBoxLayout
        self._generalLayout.addWidget(self._headerWidget)
        self._generalLayout.addWidget(self._toolsBarWidget)
        self._toolsBarWidget.setFixedHeight(70)
        self._generalLayout.addLayout(self._informationLayout)

        # TODO : Trouver comment retirer les marges dans les layouts

        self.setCentralWidget(widget)

        self.showMaximized()
        self._sceneWidget.maximized()


    def closeEvent(self, event):
        self._simulation.setAppShown(False)
