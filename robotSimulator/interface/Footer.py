from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QStatusBar, QMenuBar, QMenu, QAction, QPushButton, QLabel, QTextEdit, \
    QWidgetAction, QLineEdit

from robotSimulator.Rescaling import Rescaling
from robotSimulator.config import config


class Footer(QStatusBar):

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f9f9f9; color: #444")
        self.setLayoutDirection(Qt.LayoutDirection(1))

        fnt=QFont("Verdana", 12)
        fnt.setBold(True)

        zoomWidget = QWidget()
        zoom_layout = QHBoxLayout()
        zoomWidget.setLayout(zoom_layout)
        zoomWidget.setLayoutDirection(0)

        self._zoom_text = QLabel("100%")
        self._zoom_text.setFont(fnt)

        # TODO : QPalette ? pour gérer les couleurs

        zoom_menu = QMenuBar()
        self._zoom_menu_list = zoom_menu.addMenu("")
        self._zoom_menu_list.aboutToShow.connect(self.menuOpened)

        # actions
        zoom_in=QAction("Zoom in", self)
        zoom_in.setShortcut("ctrl++")
        zoom_in.triggered.connect(self.zoomIn) # TODO : Zoom depuis le centre

        zoom_out = QAction("Zoom out", self)
        zoom_out.setShortcut("ctrl+-")
        zoom_out.triggered.connect(self.zoomOut) # TODO : Zoom depuis le centre


        zoom_to_fit = QAction("Zoom to fit", self)
        zoom_to_fit.triggered.connect(self.zoomToFit)

        zoom_input = QWidgetAction(self)
        self._zoom_edit = QLineEdit()
        self._zoom_edit.setText("100%")
        self._zoom_edit.setStyleSheet("border: none")
        self._zoom_edit.returnPressed.connect(self.zoomInputChanged)

        zoom_input.setDefaultWidget(self._zoom_edit)
        self._zoom_menu_list.addAction(zoom_input)
        self._zoom_menu_list.addSeparator()
        self._zoom_menu_list.addAction(zoom_in)
        self._zoom_menu_list.addAction(zoom_out)
        self._zoom_menu_list.addAction(zoom_to_fit)

        self._zoom_menu_list.setLayoutDirection(Qt.LayoutDirection(0))

        zoom_menu.setStyleSheet("color : #444")

        self._zoom_menu_list.setIcon(QIcon(f"{config['ressourcesPath']}/arrow_up.svg"))

        zoom_layout.addWidget(self._zoom_text)
        zoom_layout.addWidget(zoom_menu)


        zoomWidget.setFixedWidth(112)

        pose=QWidget()
        pose_layout = QHBoxLayout()
        pose.setLayout(pose_layout)
        pose.setLayoutDirection(Qt.LayoutDirection(0))

        self._pose_text = QLabel("(0, 0)")
        self._pose_text.setFont(fnt)

        pose_icon = QLabel()
        pose_icon.setPixmap(QPixmap(f"{config['ressourcesPath']}/mousePose.svg"))

        pose_layout.addWidget(pose_icon)
        pose_layout.addWidget(self._pose_text)

        self.addPermanentWidget(pose)
        self.addPermanentWidget(zoomWidget)

    def setZoom(self):
        zoom=round(Rescaling.zoom*100)
        self._zoom_edit.setText(f"{zoom}%")
        self._zoom_text.setText(f"{zoom}%")

    def zoomIn(self):
        Rescaling.zoomIn()
        self.setZoom()

    def zoomOut(self):
        Rescaling.zoomOut()
        self.setZoom()

    def zoomToFit(self):
        Rescaling.zoomToFit()
        self.setZoom()

    def setMousePose(self, mouse):
        self._pose_text.setText(f"({mouse.x()}, {mouse.y()})")

    def zoomInputChanged(self):
        text=self._zoom_edit.text()
        if text[-1]=='%':
            text=text.rstrip(text[-1])
        if text.isnumeric():
            zoom=int(text)/100
            if Rescaling.setZoom(zoom):
                self.setZoom()
                self._zoom_menu_list.close()

    def menuOpened(self):
        self.setZoom()
        self._zoom_edit.selectAll()
        self._zoom_edit.setFocus()


