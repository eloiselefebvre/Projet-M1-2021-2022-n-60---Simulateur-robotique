from PyQt5.QtWidgets import QHBoxLayout, QMenuBar, QAction


class Header(QMenuBar):

    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()

        self.setLayout(self._layout)
        self.setStyleSheet("background-color : #f9f9f9")
        insertion = self.addMenu("Insertion")
        insertion.addAction(QAction("Random map",self))



