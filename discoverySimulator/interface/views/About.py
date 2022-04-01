from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from discoverySimulator.config import *

class About(QDialog):

    def __init__(self):
        super().__init__()
        self.setModal(True)
        layout=QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.__logo())
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(os.path.join(config["ressourcesPath"],'toolbar','about.svg')))
        self.setWindowFlags(self.windowFlags() and Qt.WindowCloseButtonHint)
        self.exec()

    def __logo(self) -> QLabel:
        widget = QLabel()
        logo = QPixmap(os.path.join(config["ressourcesPath"],'infos','popUp.svg'))
        widget.setPixmap(logo)
        return widget

