from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from robotSimulator.interface.Scene import Scene
from robotSimulator.interface.Explorer import Explorer

class Interface(QMainWindow):
    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self.setWindowTitle("Spicy Simulator")

        layout = QHBoxLayout()

        environmentWidget=Scene(self._environment)
        explorerWidget=Color('#333333')


        explorerWidget.setMaximumSize(400,1080)


        layout.addWidget(environmentWidget)
        layout.addWidget(explorerWidget)
        layout.setContentsMargins(0,0,0,0)

        widget=QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)



        self.showMaximized()





class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
