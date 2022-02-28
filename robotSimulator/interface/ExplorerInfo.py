from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from robotSimulator.config import config
from robotSimulator.representation.shapes import Rectangle
from robotSimulator.robots import Robot


class ExplorerInfo(QWidget):

    def __init__(self,environment,selectedObject):
        super().__init__()
        self._environment = environment
        self._selectedObject = selectedObject
        self.setStyleSheet("background-color: #21212F")

        self._layout=QVBoxLayout()
        self.setLayout(self._layout)

        widget=QWidget()
        self._layout.addWidget(widget)

        self._layoutInfo = QVBoxLayout()
        widget.setLayout(self._layoutInfo)

        self._layoutInfo.addWidget(self.labelInformation())
        self._layoutInfo.addWidget(self.positionInformations())
        # self._layoutInfo.addWidget(self.widthAndHeightInformations())

    def labelInformation(self):
        labelInformations=QLabel("Informations")
        labelInformations.setFixedHeight(50)
        labelInformations.setFont(QFont("Sanserif",18))
        labelInformations.setStyleSheet("color:#f9f9f9")
        return labelInformations

    def positionInformations(self):
        positionInformationsWidget=QWidget()
        positionInformationsLayout=QHBoxLayout()
        positionInformationsWidget.setLayout(positionInformationsLayout)
        positionWidget=QLabel("("+str(round(self._selectedObject.getPose().getX(),0))+","+str(round(self._selectedObject.getPose().getY(),0))+") ")
        positionWidget.setFont(QFont("Sanserif",12))
        positionWidget.setStyleSheet("color:#f9f9f9")

        positionIcon=QLabel()
        icon=QPixmap(f"{config['ressourcesPath']}/position.svg")
        positionIcon.setPixmap(icon)

        oWidget=QLabel(str(round(self._selectedObject.getPose().getOrientation(),0))+"°")
        oWidget.setFont(QFont("Sanserif",12))
        oWidget.setStyleSheet("color:#f9f9f9")

        orientationIcon = QLabel()
        icon2 = QPixmap(f"{config['ressourcesPath']}/orientation.svg")
        orientationIcon.setPixmap(icon2)

        positionInformationsLayout.addWidget(positionIcon)
        positionInformationsLayout.addWidget(positionWidget)
        positionInformationsLayout.addWidget(orientationIcon)
        positionInformationsLayout.addWidget(oWidget)

        return positionInformationsWidget

    # def widthAndHeightInformations(self):
    #     widthAndHeightInformationsWidget=QWidget()
    #     widthAndHeightInformationsLayout=QHBoxLayout()
    #     widthAndHeightInformationsWidget.setLayout(widthAndHeightInformationsLayout)
    #
    #     widthWidget = QLabel(str(round(self._selectedObject.getWidth(), 0)))
    #     widthWidget.setFont(QFont("Sanserif", 12))
    #     widthWidget.setStyleSheet("color:#f9f9f9")
    #
    #     widthIcon = QLabel()
    #     icon = QPixmap(f"{config['ressourcesPath']}/width.svg")
    #     widthIcon.setPixmap(icon)
    #
    #     if isinstance(self._selectedObject,Rectangle):
    #         heightWidget = QLabel(str(round(self._selectedObject.getHeight(), 0)))
    #         heightWidget.setFont(QFont("Sanserif", 12))
    #         heightWidget.setStyleSheet("color:#f9f9f9")
    #
    #     heightIcon = QLabel()
    #     icon2 = QPixmap(f"{config['ressourcesPath']}/height.svg")
    #     heightIcon.setPixmap(icon2)
    #
    #     widthAndHeightInformationsLayout.addWidget(widthIcon)
    #     widthAndHeightInformationsLayout.addWidget(widthWidget)
    #     widthAndHeightInformationsLayout.addWidget(heightIcon)
    #     widthAndHeightInformationsLayout.addWidget(heightWidget)
    #
    #     return widthAndHeightInformationsWidget






