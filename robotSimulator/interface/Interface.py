from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from robotSimulator.interface.Scene import Scene
from robotSimulator.interface.Explorer import Explorer
from robotSimulator.interface.ToolsBar import ToolsBar


class Interface(QMainWindow):
    def __init__(self,simulation,environment):
        super().__init__()
        self._simulation = simulation
        self._environment = environment
        self.setWindowTitle("Spicy Simulator")

        self._generalLayout = QVBoxLayout()
        self._generalLayout.setContentsMargins(0,0,0,0)
        self._informationLayout = QHBoxLayout()
        self._informationLayout.setContentsMargins(0,0,0,0)

        #self._toolsWidget=QWidget()
        self._explorerWidget=Explorer(self._environment)
        self._sceneWidget=Scene(self._environment,self._explorerWidget)
        self._toolsLayout =ToolsBar(self._environment)

        self._generalLayout.addLayout(self._toolsLayout,10)

        self._generalLayout.addLayout(self._informationLayout,90)

        self._informationLayout.addWidget(self._sceneWidget,80)
        self._informationLayout.addWidget(self._explorerWidget,20)
        self._explorerWidget.setFixedWidth(300)

        self._generalLayout.setContentsMargins(0,0,0,0)


        widget=QWidget()
        widget.setLayout(self._generalLayout)
        self.setCentralWidget(widget)

        self.showFullScreen()
        width=self._sceneWidget.width()
        height=self._sceneWidget.height()
        print(width,height)
        self._environment.drawWalls(width, height)










    def closeEvent(self, event):
        self._simulation.setAppShown(False)
