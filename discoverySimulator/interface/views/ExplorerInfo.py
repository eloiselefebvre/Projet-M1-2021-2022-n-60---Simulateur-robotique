from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from discoverySimulator import Component
from discoverySimulator.obstacles.Obstacle import Obstacle
from discoverySimulator.config import config
from discoverySimulator.interface.components.Button import VisibilityButton
from discoverySimulator.robots.Robot import Robot
from discoverySimulator.sensors.Sensor import Sensor

class ExplorerInfo(QWidget):

    def __init__(self,env,selectedObject):
        super().__init__()
        self._evironnement=env
        self._selectedObject = selectedObject
        self.setStyleSheet("background-color: #21212F;color:#f9f9f9")

        self._layout=QVBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)

        widget=QWidget()
        self._layout.addWidget(widget)

        self._layoutInfo = QVBoxLayout()
        widget.setLayout(self._layoutInfo)

        self._layoutInfo.addWidget(self.createIDWidget())
        if self._selectedObject in self._evironnement.getObjects(): # TODO : Revoir le système de construction et de rafraichissement
            self._layoutInfo.addWidget(self.positionInformations())

        if isinstance(self._selectedObject,Robot):
            self._layoutInfo.addWidget(self.showTrajectory())
            self._layoutInfo.addWidget(self.showOdometry())

        self._specificationsWidget = QLabel()
        self._specificationsWidget.setTextFormat(Qt.RichText)
        self._specificationsWidget.setFont(QFont("Sanserif", 12))
        if isinstance(self._selectedObject, Component):
            self._specificationsWidget.setText(self._selectedObject.getSpecifications())
            self._layoutInfo.addWidget(self._specificationsWidget)


    def createIDWidget(self):
        labelInformations=QWidget()
        labelInformationsLayout=QHBoxLayout()
        labelInformations.setLayout(labelInformationsLayout)

        labelIcon = QLabel()

        if isinstance(self._selectedObject,Robot):
            icon = QPixmap(f"{config['ressourcesPath']}/objects/robot.svg")
        elif isinstance(self._selectedObject,Obstacle):
            icon = QPixmap(f"{config['ressourcesPath']}/objects/obstacle.svg")
        elif isinstance(self._selectedObject,Sensor):
            icon = QPixmap(f"{config['ressourcesPath']}/objects/sensor.svg")
        else: # actuator
            icon = QPixmap(f"{config['ressourcesPath']}/objects/actuator.svg")

        labelIcon.setPixmap(icon)
        labelIcon.setFixedWidth(24)

        labelInformationsID=QLabel(self._selectedObject.getID())
        labelInformations.setFixedHeight(50)
        fnt=QFont("Sanserif",12)
        fnt.setBold(True)
        labelInformationsID.setFont(fnt)

        labelInformationsLayout.addWidget(labelIcon)
        labelInformationsLayout.addWidget(labelInformationsID)

        return labelInformations

    def refreshData(self,sender):
        if self._selectedObject in self._evironnement.getObjects():
            self._positionWidget.setText(f"({round(sender.getPose().getX())}, {round(sender.getPose().getY())})")
            self._oWidget.setText(f"{round(sender.getPose().getOrientation())}°")
        if isinstance(self._selectedObject, Component):
            self._specificationsWidget.setText(self._selectedObject.getSpecifications())

    def positionInformations(self):
        positionInformationsWidget=QWidget()

        positionInformationsLayout=QHBoxLayout(positionInformationsWidget)
        positionInformationsLayout.setContentsMargins(0, 0, 0, 0)
        positionInformationsLayout.setSpacing(0)

        # POSITION
        positionWidgetContainer=QWidget()
        positionWidgetLayout = QHBoxLayout(positionWidgetContainer)

        positionIcon=QLabel()
        icon=QPixmap(f"{config['ressourcesPath']}/infos/position.svg")
        positionIcon.setPixmap(icon)
        positionIcon.setFixedWidth(48)
        positionIcon.setStyleSheet("border:none;")

        self._positionWidget=QLabel(f"({round(self._selectedObject.getPose().getX())}, {round(self._selectedObject.getPose().getY())})")
        self._positionWidget.setFont(QFont("Sanserif",12))
        self._positionWidget.setStyleSheet("border:none;")

        positionWidgetLayout.addWidget(positionIcon)
        positionWidgetLayout.addWidget(self._positionWidget)

        # ORIENTATION
        orientationWidgetContainer = QWidget()
        orientationWidgetLayout = QHBoxLayout(orientationWidgetContainer)

        orientationIcon = QLabel()
        icon2 = QPixmap(f"{config['ressourcesPath']}/infos/orientation.svg")
        orientationIcon.setPixmap(icon2)
        orientationIcon.setFixedWidth(42)
        orientationIcon.setStyleSheet("border:none;")

        self._oWidget=QLabel(f"{round(self._selectedObject.getPose().getOrientation())}°")
        self._oWidget.setFont(QFont("Sanserif",12))
        self._oWidget.setStyleSheet("border:none;")

        orientationWidgetLayout.addWidget(orientationIcon)
        orientationWidgetLayout.addWidget(self._oWidget)


        positionInformationsLayout.addWidget(positionWidgetContainer,60)
        positionInformationsLayout.addWidget(orientationWidgetContainer,40)

        if not isinstance(self._selectedObject,Obstacle):
            positionInformationsWidget.setStyleSheet("border-bottom:2px solid #444; margin-bottom:8px; padding-bottom:12px;")

        return positionInformationsWidget

    def showTrajectory(self):
        widgetTrajectory = QWidget()
        layoutTrajectory = QHBoxLayout()
        widgetTrajectory.setLayout(layoutTrajectory)

        trajectoryLabel = QLabel("Trajectory")
        trajectoryLabel.setFont(QFont("Sanserif",12))
        trajectoryLabel.setStyleSheet("color:#f9f9f9")
        layoutTrajectory.addWidget(trajectoryLabel,90)

        self._trajectoryButton=VisibilityButton(self._selectedObject.getTrajectoryDrawn())
        self._trajectoryButton.clicked.connect(self.clickedTrajectoryButton)
        layoutTrajectory.addWidget(self._trajectoryButton)

        return widgetTrajectory

    def showOdometry(self):
        widgetOdometry = QWidget()
        layoutOdometry = QHBoxLayout()
        widgetOdometry.setLayout(layoutOdometry)

        odometryLabel = QLabel("Odometry")
        odometryLabel.setFont(QFont("Sanserif", 12))
        odometryLabel.setStyleSheet("color:#f9f9f9")
        layoutOdometry.addWidget(odometryLabel, 90)

        self._odometryButton = VisibilityButton(self._selectedObject.getOdometryDrawn())
        self._odometryButton.clicked.connect(self.clickedOdometryButton)
        layoutOdometry.addWidget(self._odometryButton)

        return widgetOdometry

    def clickedTrajectoryButton(self):
        if isinstance(self._selectedObject,Robot):
            self._selectedObject.toggleTrajectoryDrawn()
            self._trajectoryButton.setState(self._selectedObject.getTrajectoryDrawn())
            if self._selectedObject.getTrajectoryDrawn():
                self._selectedObject.showTrajectory()
            else:
                self._selectedObject.hideTrajectory()

    def clickedOdometryButton(self):
        if isinstance(self._selectedObject,Robot):
            self._selectedObject.toggleOdometryDrawn()
            self._odometryButton.setState(self._selectedObject.getOdometryDrawn())
            if self._selectedObject.getOdometryDrawn():
                self._selectedObject.showOdometry()
            else:
                self._selectedObject.hideOdometry()
