from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

from discoverySimulator.config import config


class PopUp(QDialog):

    def __init__(self):
        super().__init__()
        self.setModal(True)

        layout=QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.logo())
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(f"{config['ressourcesPath']}/toolbar/info.svg"))

        self.setWindowFlags(self.windowFlags() and Qt.WindowCloseButtonHint)
        self.exec()

    def logo(self):
        widget = QLabel()
        logo = QPixmap(f"{config['ressourcesPath']}/infos/popUp.svg")
        widget.setPixmap(logo)
        return widget

