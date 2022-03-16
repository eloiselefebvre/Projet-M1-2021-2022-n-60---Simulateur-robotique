from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QMenuBar, QAction, QLabel, \
    QWidgetAction, QLineEdit, QVBoxLayout, QToolBar

from discoverySimulator.config import config

class Footer(QToolBar):
    FOOTER_FIXED_HEIGHT = 48

    def __init__(self,zoomController):
        super().__init__()
        self._zoomController=zoomController
        self.setContentsMargins(0,0,0,0)

        self.setFixedHeight(self.FOOTER_FIXED_HEIGHT)
        self.setStyleSheet("*{background-color: #f9f9f9;color:#444;border:none;}"
                           "#widget{border-right:1px solid #C4C4C4; margin-top:8px; margin-bottom:8px;}")

        self.addWidget(self.createZoomMenuWidget())
        self.addWidget(self.createScaleWidget())
        self.addWidget(self.createMousePoseWidget())

    def createZoomMenuWidget(self):
        zoomWidget=QWidget()
        zoomWidget.setContentsMargins(12,0,12,0)
        zoomWidget.setFixedWidth(138)
        zoomWidget.setObjectName("widget")

        zoomLayout=QHBoxLayout(zoomWidget)
        zoomLayout.setAlignment(Qt.AlignCenter)

        fnt = QFont("Verdana", 12)
        fnt.setBold(True)

        self._zoom_text = QLabel("100%")
        self._zoom_text.setAlignment(Qt.AlignRight)
        self._zoom_text.setFont(fnt)
        self._zoom_text.setFixedWidth(56)

        zoomMenuBar=QMenuBar()
        zoomMenuBar.setContentsMargins(0,0,0,0)
        zoomMenuBar.setStyleSheet("QMenu::item:selected{background-color:#25CCF7;}")

        self._zoomMenu=zoomMenuBar.addMenu("")
        self._zoomMenu.aboutToShow.connect(self.menuOpened)

        self._zoomMenu.setIcon(QIcon(f"{config['ressourcesPath']}/arrowUp.svg"))

        # ACTIONS
        zoom_in = QAction("Zoom in", self)
        zoom_in.setShortcut("ctrl++")
        zoom_in.triggered.connect(self._zoomController.zoomIn)

        zoom_out = QAction("Zoom out", self)
        zoom_out.setShortcut("ctrl+-")
        zoom_out.triggered.connect(self._zoomController.zoomOut)

        zoom_to_fit = QAction("Zoom to fit", self)
        zoom_to_fit.triggered.connect(self._zoomController.zoomToFit)

        zoom_input = QWidgetAction(self)
        self._zoom_edit = QLineEdit()
        self._zoom_edit.setText("100%")
        self._zoom_edit.setStyleSheet("border: none")
        self._zoom_edit.editingFinished.connect(self.__zoomInputChanged)

        zoom_input.setDefaultWidget(self._zoom_edit)

        self._zoomMenu.addAction(zoom_input)
        self._zoomMenu.addSeparator()
        self._zoomMenu.addAction(zoom_in)
        self._zoomMenu.addAction(zoom_out)
        self._zoomMenu.addAction(zoom_to_fit)

        zoomLayout.addWidget(self._zoom_text)
        zoomLayout.addWidget(zoomMenuBar)

        return zoomWidget


    def createScaleWidget(self):
        scaleWidget = QWidget()
        scaleWidget.setObjectName("widget")
        scaleLayout = QVBoxLayout(scaleWidget)
        scaleLayout.setSpacing(0)
        self._scale_text = QLabel("100")
        fnt = QFont("Verdana", 10)
        fnt.setBold(True)
        self._scale_text.setFont(fnt)
        self._scale_text.setAlignment(Qt.AlignCenter)
        scaleIcon = QLabel()
        scaleIcon.setPixmap(QPixmap(f"{config['ressourcesPath']}scale.svg"))
        scaleIcon.setFixedSize(100, 12)

        scaleLayout.addWidget(self._scale_text)
        scaleLayout.addWidget(scaleIcon)

        scaleLayout.setSpacing(0)
        scaleWidget.setContentsMargins(12, 0, 12, 0)

        return scaleWidget

    def createMousePoseWidget(self):
        poseWidget = QWidget()
        poseLayout = QHBoxLayout()
        poseWidget.setLayout(poseLayout)
        poseWidget.setLayoutDirection(Qt.LayoutDirection(0))

        fnt = QFont("Verdana", 12)
        fnt.setBold(True)
        self._pose_text = QLabel("(0, 0)")
        self._pose_text.setStyleSheet("margin-left:8px;")
        self._pose_text.setFont(fnt)

        poseIcon = QLabel()
        poseIcon.setPixmap(QPixmap(f"{config['ressourcesPath']}/mousePose.svg"))

        poseLayout.addWidget(poseIcon)
        poseLayout.addWidget(self._pose_text)

        poseLayout.setSpacing(0)
        poseWidget.setContentsMargins(12,0,12,0)

        return poseWidget

    def updateZoom(self,sender):
        zoom=round(sender.getZoom()*100)
        self._zoom_edit.setText(f"{zoom}%")
        self._zoom_text.setText(f"{zoom}%")
        self._scale_text.setText(str(round(100/sender.getZoom())))

    def updateMousePoseFromScene(self,scene):
        mouse=scene.mousePose()
        self._pose_text.setText(f"({mouse.x()}, {mouse.y()})")

    def __zoomInputChanged(self):
        text=self._zoom_edit.text()
        if text[-1]=='%':
            text=text.rstrip('%')
        if text.isnumeric():
            zoom=int(text)/100
            if self._zoomController.setZoom(zoom):
                self._zoomMenu.close()
        else:
            self._zoom_edit.setText(f"{int(self._zoomController.getZoom()*100)}%")

    def menuOpened(self):
        self._zoom_edit.selectAll()
        self._zoom_edit.setFocus()


# class Footer(QStatusBar):
#
#     FOOTER_FIXED_HEIGHT = 48
#
#     def __init__(self,zoomController):
#         super().__init__()
#         self._zoomController=zoomController
#
#         self.setFixedHeight(self.FOOTER_FIXED_HEIGHT)
#         self.setLayoutDirection(Qt.LayoutDirection(1))
#
#         fnt=QFont("Verdana", 12)
#         fnt.setBold(True)
#
#         zoomWidget = QWidget()
#
#         zoom_layout = QHBoxLayout(zoomWidget)
#         zoom_layout.setSpacing(0)
#         zoomWidget.setLayoutDirection(0)
#
#         self._zoom_text = QLabel("100%")
#         self._zoom_text.setFont(fnt)
#
#         zoom_menu = QMenuBar()
#         self._zoom_menu_list = zoom_menu.addMenu("")
#         self._zoom_menu_list.setIcon(QIcon(f"{config['ressourcesPath']}/arrowUp.svg"))
#         self._zoom_menu_list.aboutToShow.connect(self.menuOpened)
#
        # # actions
        # zoom_in=QAction("Zoom in", self)
        # zoom_in.setShortcut("ctrl++")
        # zoom_in.triggered.connect(self._zoomController.zoomIn)
        #
        # zoom_out = QAction("Zoom out", self)
        # zoom_out.setShortcut("ctrl+-")
        # zoom_out.triggered.connect(self._zoomController.zoomOut)
        #
        # zoom_to_fit = QAction("Zoom to fit", self)
        # zoom_to_fit.triggered.connect(self._zoomController.zoomToFit)
        #
        # zoom_input = QWidgetAction(self)
        # self._zoom_edit = QLineEdit()
        # self._zoom_edit.setText("100%")
        # self._zoom_edit.setStyleSheet("border: none")
        # self._zoom_edit.returnPressed.connect(self.zoomInputChanged)
        #
        # zoom_input.setDefaultWidget(self._zoom_edit)
        # self._zoom_menu_list.addAction(zoom_input)
        # self._zoom_menu_list.addSeparator()
        # self._zoom_menu_list.addAction(zoom_in)
        # self._zoom_menu_list.addAction(zoom_out)
        # self._zoom_menu_list.addAction(zoom_to_fit)
#
#         self._zoom_menu_list.setLayoutDirection(Qt.LayoutDirection(0))
#
#         zoom_menu.setStyleSheet("*{color : #444;}"
#                                 "QMenu::item:selected{background-color:#25CCF7;}"
#                                 ) # "QMenuBar:hover{background:red;}"
#
#         zoom_layout.addWidget(self._zoom_text)
#         zoom_layout.addWidget(zoom_menu)
#
#         zoomWidget.setFixedWidth(142)
#
#
        # pose=QWidget()
        # pose_layout = QHBoxLayout()
        # pose.setLayout(pose_layout)
        # pose.setLayoutDirection(Qt.LayoutDirection(0))
        #
        # self._pose_text = QLabel("(0, 0)")
        # self._pose_text.setFont(fnt)
        #
        # pose_icon = QLabel()
        # pose_icon.setPixmap(QPixmap(f"{config['ressourcesPath']}/mousePose.svg"))
        #
        # pose_layout.addWidget(pose_icon)
        # pose_layout.addWidget(self._pose_text)
#
        # scale=QWidget()
        # scale_layout=QVBoxLayout(scale)
        # scale_layout.setSpacing(0)
        # self._scale_text=QLabel("100")
        # fnt=QFont("Verdana",10)
        # fnt.setBold(True)
        # self._scale_text.setFont(fnt)
        # self._scale_text.setAlignment(Qt.AlignCenter)
        # scale_icon = QLabel()
        # scale_icon.setPixmap(QPixmap(f"{config['ressourcesPath']}/scale.svg"))
        # scale_icon.setFixedSize(100,12)
        #
        # scale_layout.addWidget(self._scale_text)
        # scale_layout.addWidget(scale_icon)
#
#         pose.setContentsMargins(12,0,12,0)
#         scale.setContentsMargins(12,0,12,0)
#         zoomWidget.setContentsMargins(12,0,12,0)
#         self.addPermanentWidget(pose)
#         self.addPermanentWidget(scale)
#         self.addPermanentWidget(zoomWidget)
#         self.setStyleSheet("background-color: #f9f9f9; color: #444;")
#
    # def updateZoom(self,sender):
    #     zoom=round(sender.getZoom()*100)
    #     self._zoom_edit.setText(f"{zoom}%")
    #     self._zoom_text.setText(f"{zoom}%")
    #     self._scale_text.setText(str(round(100/sender.getZoom())))
    #
    # def updateMousePoseFromScene(self,scene):
    #     mouse=scene.mousePose()
    #     self._pose_text.setText(f"({mouse.x()}, {mouse.y()})")
    #
    # def zoomInputChanged(self):
    #     text=self._zoom_edit.text()
    #     if text[-1]=='%':
    #         text=text.rstrip('%')
    #     if text.isnumeric():
    #         zoom=int(text)/100
    #         if self._zoomController.setZoom(zoom):
    #             self._zoom_menu_list.close()
    #     else:
    #         self._zoom_edit.setText(f"{int(self._zoomController.getZoom()*100)}%")
    #
    # def menuOpened(self):
    #     self._zoom_edit.selectAll()
    #     self._zoom_edit.setFocus()