from PyQt5.QtWidgets import QMenuBar, QAction, QPushButton


class MenuBar(QMenuBar):

    def __init__(self):
        super().__init__()
        self._menuBar = QMenuBar()
        self._menuBar.setStyleSheet("#F0F0F0")



