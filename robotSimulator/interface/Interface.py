from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTextEdit
from robotSimulator.interface.Scene import Scene
from robotSimulator.interface.Explorer import Explorer

class Interface(QMainWindow):
    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self.setWindowTitle("Spicy Simulator")

        layout = QHBoxLayout()
        explorerLayout=QVBoxLayout()

        environmentWidget=Scene(self._environment)
        explorerWidget=Explorer(self._environment)

        valuesWidget=QTextEdit()
        valuesWidget.setText(explorerWidget.printObjects())

        explorerWidget.setMaximumSize(400,1080)

        layout.addWidget(environmentWidget)
        layout.addWidget(explorerWidget)
        explorerLayout.addWidget(valuesWidget)
        layout.setContentsMargins(0,0,0,0)

        widget=QWidget()
        explorerWidget.setLayout(explorerLayout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.showMaximized()




