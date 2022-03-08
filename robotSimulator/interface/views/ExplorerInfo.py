from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from robotSimulator.Obstacle import Obstacle
from robotSimulator.config import config
from robotSimulator.interface.componants.Button import VisibilityButton
from robotSimulator.robots.Robot import Robot
from robotSimulator.sensors.Sensor import Sensor


class ExplorerInfo(QWidget):

    def __init__(self,selectedObject):
        super().__init__()
        self._selectedObject = selectedObject
        self.setStyleSheet("background-color: #21212F")

        self._layout=QVBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)

        widget=QWidget()
        self._layout.addWidget(widget)

        self._layoutInfo = QVBoxLayout()
        widget.setLayout(self._layoutInfo)

        self._layoutInfo.addWidget(self.labelInformation())
        self._layoutInfo.addWidget(self.positionInformations())

        if isinstance(self._selectedObject,Robot):
            self._layoutInfo.addWidget(self.showTrajectory())
            self._layoutInfo.addWidget(self.showOdometry())

    def labelInformation(self):
        labelInformations=QWidget()
        labelInformationsLayout=QHBoxLayout()
        labelInformations.setLayout(labelInformationsLayout)

        labelIcon = QLabel()
        icon=None

        if isinstance(self._selectedObject,Robot):
            icon = QPixmap(f"{config['ressourcesPath']}/robot.svg")

        if isinstance(self._selectedObject,Obstacle):
            icon = QPixmap(f"{config['ressourcesPath']}/obstacle.svg")

        if isinstance(self._selectedObject,Sensor):
            icon = QPixmap(f"{config['ressourcesPath']}/sensor.svg")

        labelIcon.setPixmap(icon)
        labelIcon.setFixedWidth(50)

        labelInformationsID=QLabel(self._selectedObject.getID())
        labelInformations.setFixedHeight(50)
        labelInformations.setFont(QFont("Sanserif",30))
        labelInformations.setStyleSheet("color:#f9f9f9")

        labelInformationsLayout.addWidget(labelIcon)
        labelInformationsLayout.addWidget(labelInformationsID)

        return labelInformations

    def refreshData(self,sender):
        self._positionWidget.setText("("+str(round(sender.getPose().getX(),0))+","+str(round(sender.getPose().getY(),0))+") ")
        self._oWidget.setText(str(round(sender.getPose().getOrientation(),0))+"°")

    def positionInformations(self):
        positionInformationsWidget=QWidget()
        positionInformationsLayout=QHBoxLayout()
        positionInformationsWidget.setLayout(positionInformationsLayout)
        self._positionWidget=QLabel("("+str(round(self._selectedObject.getPose().getX(),0))+","+str(round(self._selectedObject.getPose().getY(),0))+") ")
        self._positionWidget.setFont(QFont("Sanserif",12))
        self._positionWidget.setStyleSheet("color:#f9f9f9")

        positionIcon=QLabel()
        icon=QPixmap(f"{config['ressourcesPath']}/position.svg")
        positionIcon.setPixmap(icon)

        self._oWidget=QLabel(str(round(self._selectedObject.getPose().getOrientation(),0))+"°")
        self._oWidget.setFont(QFont("Sanserif",12))
        self._oWidget.setStyleSheet("color:#f9f9f9")

        orientationIcon = QLabel()
        icon2 = QPixmap(f"{config['ressourcesPath']}/orientation.svg")
        orientationIcon.setPixmap(icon2)

        positionInformationsLayout.addWidget(positionIcon)
        positionInformationsLayout.addWidget(self._positionWidget)
        positionInformationsLayout.addWidget(orientationIcon)
        positionInformationsLayout.addWidget(self._oWidget)

        return positionInformationsWidget

    def showTrajectory(self):
        widgetTrajectory = QWidget()
        layoutTrajectory = QHBoxLayout()
        widgetTrajectory.setLayout(layoutTrajectory)

        trajectoryLabel = QLabel("Trajectory")
        trajectoryLabel.setFont(QFont("Sanserif",15))
        trajectoryLabel.setStyleSheet("color:#f9f9f9")
        layoutTrajectory.addWidget(trajectoryLabel,90)

        self._trajectoryButton=VisibilityButton(self._selectedObject.getTrajectoryDrawn())
        self._trajectoryButton.clicked.connect(self.clickedTrajectoryButton)
        layoutTrajectory.addWidget(self._trajectoryButton,10)

        return widgetTrajectory

    def showOdometry(self):
        widgetOdometry = QWidget()
        layoutOdometry = QHBoxLayout()
        widgetOdometry.setLayout(layoutOdometry)

        odometryLabel = QLabel("Odometry")
        odometryLabel.setFont(QFont("Sanserif", 15))
        odometryLabel.setStyleSheet("color:#f9f9f9")
        layoutOdometry.addWidget(odometryLabel, 90)

        self._odometryButton = VisibilityButton(self._selectedObject.getOdometryDrawn())
        self._odometryButton.clicked.connect(self.clickedOdometryButton)
        layoutOdometry.addWidget(self._odometryButton, 10)

        return widgetOdometry

    def clickedTrajectoryButton(self):
        if isinstance(self._selectedObject,Robot):
            self._selectedObject.toggleTrajectoryDrawn()
            self._trajectoryButton.setVisibleObject(self._selectedObject.getTrajectoryDrawn())
            if self._selectedObject.getTrajectoryDrawn():
                self._selectedObject.showTrajectory()
            else:
                self._selectedObject.hideTrajectory()

    def clickedOdometryButton(self):
        if isinstance(self._selectedObject,Robot):
            self._selectedObject.toggleOdometryDrawn()
            self._odometryButton.setVisibleObject(self._selectedObject.getOdometryDrawn())
            if self._selectedObject.getOdometryDrawn():
                self._selectedObject.showOdometry()
            else:
                self._selectedObject.hideOdometry()
