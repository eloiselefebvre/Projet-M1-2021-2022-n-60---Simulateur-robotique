from PyQt5.QtCore import Qt, QPoint, QMargins
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from discoverySimulator.config import colors


class SceneOverview(QWidget):

    def __init__(self,environment,zoomController):
        super().__init__()
        self.setContentsMargins(12,12,12,12)
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet(f"background-color: {colors['alabaster']} ; border: 2px solid "+colors['salmon']+"; border-radius: 8px; margin:12px")
        layout=QHBoxLayout(self)
        layout.setSpacing(0)

        self.__sceneOverviewContent = SceneOverviewContent(environment,zoomController)
        layout.addWidget(self.__sceneOverviewContent)

    def size(self):
        return self.__sceneOverviewContent.size()


class SceneOverviewContent(QWidget):
    __SCENE_OVERVIEW_WIDTH  = 280
    __SCENE_OVERVIEW_RATIO  = 16/9

    def __init__(self,environment,zoomController):
        super().__init__()
        self.__environment = environment
        self.__zoomController=zoomController
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("border:none; border-radius:0; margin:0;")

        self.setFixedSize(SceneOverviewContent.__SCENE_OVERVIEW_WIDTH,round(SceneOverviewContent.__SCENE_OVERVIEW_WIDTH/SceneOverviewContent.__SCENE_OVERVIEW_RATIO))

        self.__dragView = False
        self.__dragViewOrigin = QPoint(0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        offset = self.__zoomController.getOverviewOffset()
        painter.translate(offset.x(), offset.y())
        painter.scale(self.__zoomController.getZoomOverview(), self.__zoomController.getZoomOverview())

        objects = self.__environment.getVirtualObjects().copy()
        objects.extend(self.__environment.getObjects())
        objects.sort(key=lambda obj: obj.getZIndex())

        for obj in objects:
            painter.save()
            obj.paint(painter)
            painter.restore()

        color = QColor(colors['blue-violet'])
        painter.setPen(QPen(color,8, Qt.SolidLine))

        offset = -self.__zoomController.getOffset() / self.__zoomController.getZoom()
        ox=int(offset.x())
        oy=int(offset.y())

        sceneSize=self.__zoomController.getSceneSize()
        w=int(sceneSize.width() / self.__zoomController.getZoom())
        h=int(sceneSize.height() / self.__zoomController.getZoom())

        painter.drawRect(ox,oy,w,h)

        color.setAlpha(48)
        painter.setBrush(QBrush(color, Qt.SolidPattern))
        painter.drawRect(ox,oy,w,h)

    def mousePressEvent(self,event):
        self.setCursor(Qt.ClosedHandCursor)
        if event.button() == Qt.LeftButton:
            self.__viewGrabbed(event.pos())

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        self.__dragView=False

    def mouseMoveEvent(self,event):
        if self.__dragView:
            current=(event.pos() - self.__zoomController.getOverviewOffset())/self.__zoomController.getZoomOverview()
            self.__zoomController.setOffset(self.__zoomController.getOffset() - (current - self.__dragViewOrigin) * self.__zoomController.getZoom())
            self.__dragViewOrigin = current

    def __viewGrabbed(self, mouse):
        mouseRescale = (mouse - self.__zoomController.getOverviewOffset()) / self.__zoomController.getZoomOverview()
        offset = self.__zoomController.getOffset()
        sceneSize = self.__zoomController.getSceneSize()
        bx = -offset.x()/ self.__zoomController.getZoom()
        by = -offset.y()/ self.__zoomController.getZoom()

        ex = bx + sceneSize.width()
        ey = by + sceneSize.height()

        if mouseRescale.x() > bx and mouseRescale.y() > by and mouseRescale.x() < ex and mouseRescale.y() < ey:
            self.__dragView = True
            self.__dragViewOrigin = mouseRescale