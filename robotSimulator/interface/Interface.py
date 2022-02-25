from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from robotSimulator.interface.ExplorerInfo import ExplorerInfo
from robotSimulator.interface.Scene import Scene
from robotSimulator.interface.Explorer import Explorer
from robotSimulator.interface.ToolsBar import ToolsBar


class Interface(QMainWindow):
    def __init__(self,simulation,environment):
        super().__init__()
        self._simulation = simulation
        self._environment = environment
        self.setWindowTitle("Spicy Simulator")

        # layout généraux
        self._generalLayout = QVBoxLayout()
        self._generalLayout.setContentsMargins(0,0,0,0)
        self._informationLayout = QHBoxLayout()
        self._informationLayout.setContentsMargins(0,0,0,0)
        self._informationLayout.setSpacing(0)


        widget=QWidget()
        widget.setLayout(self._generalLayout)

        #widget explorer
        self._explorerWidget = QWidget()
        self._explorerLayout=QVBoxLayout()
        self._explorerWidget.setLayout(self._explorerLayout)
        self._explorerTreeWidget=Explorer(self._environment)
        self._explorerLayout.addWidget(self._explorerTreeWidget,80)
        self._explorerInfoWidget = ExplorerInfo(self._environment)
        self._explorerLayout.addWidget(self._explorerInfoWidget,20)

        self._sceneWidget=Scene(self._environment,self._explorerTreeWidget)
        self._toolsLayout =ToolsBar(self._environment,self._simulation)
        self._toolsLayout.setSpacing(0)
        self._explorerLayout.setSpacing(0)

        self._informationLayout.addWidget(self._sceneWidget,90)
        self._informationLayout.addWidget(self._explorerWidget,10)

        #ajout des deux layout du QVBoxLayout
        self._generalLayout.addLayout(self._toolsLayout,10)
        self._generalLayout.addLayout(self._informationLayout,90)

        self._generalLayout.setContentsMargins(0,0,0,0)
        self._generalLayout.setSpacing(0)
        # TODO : Trouver comment retirer les marges dans les layouts

        self.setCentralWidget(widget)

        self.showMaximized()
        self._sceneWidget.maximized()


    def closeEvent(self, event):
        self._simulation.setAppShown(False)
