from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

from robotSimulator.config import config


class PopUp(QDialog):

    def __init__(self):
        super().__init__()
        self.setModal(True)

        layout=QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.logo())
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(f"{config['ressourcesPath']}/info.svg"))
        self.exec()

    def logo(self):
        widget = QLabel()
        logo = QPixmap(f"{config['ressourcesPath']}/popUp.svg")
        widget.setPixmap(logo)
        return widget

