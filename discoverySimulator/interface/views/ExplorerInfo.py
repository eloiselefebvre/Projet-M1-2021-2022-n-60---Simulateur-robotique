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

    def __init__(self, environment, selectedObject):
        super().__init__()
        self.__evironnement=environment
        self.__selectedObject = selectedObject
        self.setStyleSheet("background-color: #21212F;color:#f9f9f9")

        self.__layout=QVBoxLayout(self)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        widget=QWidget()
        self.__layout.addWidget(widget)

        self.__layoutInfo = QVBoxLayout()
        widget.setLayout(self.__layoutInfo)

        self.__layoutInfo.addWidget(self.__createIDWidget())
        if self.__selectedObject in self.__evironnement.getObjects(): # TODO : Revoir le système de construction et de rafraichissement
            self.__layoutInfo.addWidget(self.positionInformations())

        if isinstance(self.__selectedObject, Robot):
            self.__layoutInfo.addWidget(self.showTrajectory())
            self.__layoutInfo.addWidget(self.__showOdometry())

        self.__specificationsWidget = QLabel()
        self.__specificationsWidget.setTextFormat(Qt.RichText)
        self.__specificationsWidget.setFont(QFont("Sanserif", 12))
        if isinstance(self.__selectedObject, Component):
            self.__specificationsWidget.setText(self.__selectedObject.getSpecifications())
            self.__layoutInfo.addWidget(self.__specificationsWidget)

    def showTrajectory(self):
        widgetTrajectory = QWidget()
        layoutTrajectory = QHBoxLayout()
        widgetTrajectory.setLayout(layoutTrajectory)

        trajectoryLabel = QLabel("Trajectory")
        trajectoryLabel.setFont(QFont("Sanserif",12))
        trajectoryLabel.setStyleSheet("color:#f9f9f9")
        layoutTrajectory.addWidget(trajectoryLabel,90)

        self.__trajectoryButton=VisibilityButton(self.__selectedObject.getTrajectoryDrawn())
        self.__trajectoryButton.clicked.connect(self.__clickedTrajectoryButton)
        layoutTrajectory.addWidget(self.__trajectoryButton)

        return widgetTrajectory

    def refreshData(self,sender):
        if self.__selectedObject in self.__evironnement.getObjects():
            self.__positionWidget.setText(f"({round(sender.getPose().getX())}, {round(sender.getPose().getY())})")
            self.__oWidget.setText(f"{round(sender.getPose().getOrientation())}°")
        if isinstance(self.__selectedObject, Component):
            self.__specificationsWidget.setText(self.__selectedObject.getSpecifications())

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

        self.__positionWidget=QLabel(f"({round(self.__selectedObject.getPose().getX())}, {round(self.__selectedObject.getPose().getY())})")
        self.__positionWidget.setFont(QFont("Sanserif", 12))
        self.__positionWidget.setStyleSheet("border:none;")

        positionWidgetLayout.addWidget(positionIcon)
        positionWidgetLayout.addWidget(self.__positionWidget)

        # ORIENTATION
        orientationWidgetContainer = QWidget()
        orientationWidgetLayout = QHBoxLayout(orientationWidgetContainer)

        orientationIcon = QLabel()
        icon2 = QPixmap(f"{config['ressourcesPath']}/infos/orientation.svg")
        orientationIcon.setPixmap(icon2)
        orientationIcon.setFixedWidth(42)
        orientationIcon.setStyleSheet("border:none;")

        self.__oWidget=QLabel(f"{round(self.__selectedObject.getPose().getOrientation())}°")
        self.__oWidget.setFont(QFont("Sanserif", 12))
        self.__oWidget.setStyleSheet("border:none;")

        orientationWidgetLayout.addWidget(orientationIcon)
        orientationWidgetLayout.addWidget(self.__oWidget)


        positionInformationsLayout.addWidget(positionWidgetContainer,60)
        positionInformationsLayout.addWidget(orientationWidgetContainer,40)

        if not isinstance(self.__selectedObject, Obstacle):
            positionInformationsWidget.setStyleSheet("border-bottom:2px solid #444; margin-bottom:8px; padding-bottom:12px;")

        return positionInformationsWidget

    def __createIDWidget(self):
        labelInformations=QWidget()
        labelInformationsLayout=QHBoxLayout()
        labelInformations.setLayout(labelInformationsLayout)
        labelIcon = QLabel()

        if isinstance(self.__selectedObject, Robot):
            icon = QPixmap(f"{config['ressourcesPath']}/objects/robot.svg")
        elif isinstance(self.__selectedObject, Obstacle):
            icon = QPixmap(f"{config['ressourcesPath']}/objects/obstacle.svg")
        elif isinstance(self.__selectedObject, Sensor):
            icon = QPixmap(f"{config['ressourcesPath']}/objects/sensor.svg")
        else: # actuator
            icon = QPixmap(f"{config['ressourcesPath']}/objects/actuator.svg")

        labelIcon.setPixmap(icon)
        labelIcon.setFixedWidth(24)

        labelInformationsID=QLabel(self.__selectedObject.getID())
        labelInformations.setFixedHeight(50)
        fnt=QFont("Sanserif",12)
        fnt.setBold(True)
        labelInformationsID.setFont(fnt)

        labelInformationsLayout.addWidget(labelIcon)
        labelInformationsLayout.addWidget(labelInformationsID)

        return labelInformations

    def __showOdometry(self):
        widgetOdometry = QWidget()
        layoutOdometry = QHBoxLayout()
        widgetOdometry.setLayout(layoutOdometry)

        odometryLabel = QLabel("Odometry")
        odometryLabel.setFont(QFont("Sanserif", 12))
        odometryLabel.setStyleSheet("color:#f9f9f9")
        layoutOdometry.addWidget(odometryLabel, 90)

        self.__odometryButton = VisibilityButton(self.__selectedObject.getOdometryDrawn())
        self.__odometryButton.clicked.connect(self.__clickedOdometryButton)
        layoutOdometry.addWidget(self.__odometryButton)

        return widgetOdometry

    def __clickedTrajectoryButton(self):
        if isinstance(self.__selectedObject, Robot):
            self.__selectedObject.toggleTrajectoryDrawn()
            self.__trajectoryButton.setState(self.__selectedObject.getTrajectoryDrawn())
            if self.__selectedObject.getTrajectoryDrawn():
                self.__selectedObject.showTrajectory()
            else:
                self.__selectedObject.hideTrajectory()

    def __clickedOdometryButton(self):
        if isinstance(self.__selectedObject, Robot):
            self.__selectedObject.toggleOdometryDrawn()
            self.__odometryButton.setState(self.__selectedObject.getOdometryDrawn())
            if self.__selectedObject.getOdometryDrawn():
                self.__selectedObject.showOdometry()
            else:
                self.__selectedObject.hideOdometry()
