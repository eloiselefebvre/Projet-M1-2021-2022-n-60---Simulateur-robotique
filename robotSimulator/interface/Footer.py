from PyQt5.QtWidgets import QHBoxLayout, QWidget


class Footer(QWidget):

    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()
        self.setStyleSheet("background-color: #f00") # f9f9f9
        self.setFixedHeight(64)
