from PyQt5.QtCore import Qt, QPoint, QMargins
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from discoverySimulator.config import colors


class SceneOverview(QWidget):

    __SCENE_OVERVIEW_WIDTH  = 320
    __SCENE_OVERVIEW_RATIO  = 16/9
    __SCENE_OVERVIEW_CONTENT_MARGIN = 12

    def __init__(self,environment,zoomController):
        super().__init__()
        self.setFixedSize(SceneOverview.__SCENE_OVERVIEW_WIDTH,round(SceneOverview.__SCENE_OVERVIEW_WIDTH/SceneOverview.__SCENE_OVERVIEW_RATIO))
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setContentsMargins(SceneOverview.__SCENE_OVERVIEW_CONTENT_MARGIN, SceneOverview.__SCENE_OVERVIEW_CONTENT_MARGIN, SceneOverview.__SCENE_OVERVIEW_CONTENT_MARGIN, SceneOverview.__SCENE_OVERVIEW_CONTENT_MARGIN)
        self.setStyleSheet(f"background-color: {colors['font']} ; border: 2px solid "+colors['sceneOverviewBorder']+"; border-radius: 8px; margin:12px;")

        layout=QHBoxLayout(self)
        layout.addWidget(SceneOverviewContent(environment,zoomController))

    def size(self):
        return super().size().grownBy(-QMargins(SceneOverview.__SCENE_OVERVIEW_CONTENT_MARGIN, SceneOverview.__SCENE_OVERVIEW_CONTENT_MARGIN, SceneOverview.__SCENE_OVERVIEW_CONTENT_MARGIN, SceneOverview.__SCENE_OVERVIEW_CONTENT_MARGIN))


class SceneOverviewContent(QWidget):

    def __init__(self,environment,zoomController):
        super().__init__()
        self.__environment = environment
        self.__zoomController=zoomController

        self.__dragView = False
        self.__dragViewOrigin = QPoint(0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self.__zoomController.getMiniZoom(), self.__zoomController.getMiniZoom())
        objects = self.__environment.getVirtualObjects().copy()
        objects.extend(self.__environment.getObjects())
        objects.sort(key=lambda obj: obj.getZIndex())

        for obj in objects:
            painter.save()
            obj.paint(painter)
            painter.restore()

        painter.setPen(QPen(QColor(colors['painter']),8, Qt.SolidLine))

        offset = -self.__zoomController.getOffset() / self.__zoomController.getZoom()
        ox=int(offset.x())
        oy=int(offset.y())

        sceneSize=self.__zoomController.getSceneSize()
        w=int(sceneSize.width() / self.__zoomController.getZoom())
        h=int(sceneSize.height() / self.__zoomController.getZoom())

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
            current=event.pos()/self.__zoomController.getMiniZoom()
            self.__zoomController.setOffset(self.__zoomController.getOffset() - (current - self.__dragViewOrigin) * self.__zoomController.getZoom())
            self.__dragViewOrigin = current


    def __viewGrabbed(self, mouse):
        mouseRescale = mouse / self.__zoomController.getMiniZoom()
        offset = self.__zoomController.getOffset()
        sceneSize = self.__zoomController.getSceneSize()
        bx = -offset.x() / self.__zoomController.getZoom()
        by = -offset.y() / self.__zoomController.getZoom()
        ex = bx + sceneSize.width()
        ey = by + sceneSize.height()

        if mouseRescale.x() > bx and mouseRescale.y() > by and mouseRescale.x() < ex and mouseRescale.y() < ey:
            self.__dragView = True
            self.__dragViewOrigin = mouseRescale