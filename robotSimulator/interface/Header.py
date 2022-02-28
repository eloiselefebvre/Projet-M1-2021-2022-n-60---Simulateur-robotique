from PyQt5.QtWidgets import QHBoxLayout, QMenuBar


class Header(QMenuBar):

    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()

        self.setLayout(self._layout)
        self.setStyleSheet("background-color : #f9f9f9")
        self.addMenu("Maps")



