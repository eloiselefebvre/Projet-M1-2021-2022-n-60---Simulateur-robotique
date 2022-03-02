from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget

class SceneOverview(QWidget):

    def __init__(self,environment,zoomController):
        super().__init__()
        self._environment = environment
        self._zoomController=zoomController

        self.setStyleSheet("background-color: #f0f0f0")

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.scale(self._zoomController.getMiniZoom(),self._zoomController.getMiniZoom())
        for obj in self._environment.getObjects():
            painter.save()
            obj.paint(painter)
            painter.restore()

        for obj in self._environment.getVirtualObjects():
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
