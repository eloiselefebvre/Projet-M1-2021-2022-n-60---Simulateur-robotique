from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLayout
from discoverySimulator.config import *

class About(QDialog):

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(os.path.join(config["ressourcesPath"],'toolbar','about.svg')))
        self.setWindowFlags(self.windowFlags() and Qt.WindowCloseButtonHint)

        layout=QVBoxLayout()
        layout.addWidget(self.__createPanelWidget())
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

        self.exec()

    def __createPanelWidget(self) -> QLabel:
        return QSvgWidget(os.path.join(config["ressourcesPath"],'infos','creditPanel.svg'))

