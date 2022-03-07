from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget

class SceneOverview(QWidget):

    def __init__(self,environment,zoomController): # TODO : Rafraichir l'affichage du drag même en pause
        super().__init__()
        self._environment = environment
        self._zoomController=zoomController

        self._dragView=False
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)

        self._dragViewOrigin = QPoint(0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self._zoomController.getMiniZoom(),self._zoomController.getMiniZoom())

        objects = self._environment.getVirtualObjects().copy()
        objects.extend(self._environment.getObjects())
        objects.sort(key=lambda obj: obj.getZIndex())

        for obj in objects:
            painter.save()
            obj.paint(painter)
            painter.restore()

        painter.setPen(QPen(QColor("#675BB5"),8, Qt.SolidLine))

        offset = -self._zoomController.getOffset()/self._zoomController.getZoom()
        ox=int(offset.x())
        oy=int(offset.y())

        sceneSize=self._zoomController.getSceneSize()
        w=int(sceneSize.width()/self._zoomController.getZoom())
        h=int(sceneSize.height()/self._zoomController.getZoom())

        painter.drawRect(ox,oy,w,h)

    def mousePressEvent(self,event):
        self.setCursor(Qt.ClosedHandCursor)
        if event.button() == Qt.LeftButton:
            self._viewGrabbed(event.pos())

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        self._dragView=False

    def _viewGrabbed(self,mouse):
        mouseRescale = mouse/self._zoomController.getMiniZoom()
        offset = self._zoomController.getOffset()
        sceneSize=self._zoomController.getSceneSize()
        bx=-offset.x() # begin x
        by=-offset.y()
        ex = bx+sceneSize.width()
        ey = by+sceneSize.height()

        if mouseRescale.x()>bx and mouseRescale.y()>by and mouseRescale.x()<ex and mouseRescale.y()<ey:
            self._dragView=True
            self._dragViewOrigin=mouseRescale

    def mouseMoveEvent(self,event):
        if self._dragView:
            current=event.pos()/self._zoomController.getMiniZoom()
            self._zoomController.setOffset(self._zoomController.getOffset() - (current - self._dragViewOrigin))
            self._dragViewOrigin = current

