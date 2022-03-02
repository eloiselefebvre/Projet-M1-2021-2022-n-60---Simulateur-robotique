from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint

from robotSimulator.Observable import Observable
from robotSimulator.Rescaling import Rescaling
from robotSimulator.robots.Robot import Robot


class Scene(QWidget,Observable):

    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self._explorer=None
        self._dragObject=False
        self._dragScene = False
        self._dragSceneOrigin=QPoint(0,0)
        self._selectedObj = None
        self._selectionOffset=(0,0)
        self._maximized = False
        self._size=None
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)

        self.setStyleSheet("background-color: #f0f0f0")

        self._convertedMousePose=QPoint(0, 0)


    def defineExplorer(self,explorer):
        self._explorer=explorer

    def refreshView(self,sender):
        self.update()

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.translate(Rescaling.offsetX, Rescaling.offsetY)
        painter.scale(Rescaling.zoom, Rescaling.zoom)

        for obj in self._environment.getObjects():
            painter.save()
            obj.paint(painter)
            painter.restore()

        for obj in self._environment.getVirtualObjects():
            painter.save()
            obj.paint(painter)
            painter.restore()

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        if event.button()==Qt.LeftButton:
            self._isClickedObject(event.pos())
            self._dragObject=True

        if event.button() == Qt.MiddleButton:
            self._dragScene = True
            self._dragSceneOrigin = event.pos()

    def mouseReleaseEvent(self,event):
        self.setCursor(Qt.OpenHandCursor)
        self._dragObject=False
        self._dragScene=False
        if self._selectedObj is not None:
            self._selectedObj.setCollidedState(False)
            self._selectedObj = None

    def mousePose(self):
        return self._convertedMousePose

    def mouseMoveEvent(self, event):
        self._convertedMousePose = (event.pos() - Rescaling.getOffset()) / Rescaling.zoom
        self.notifyObservers()
        if self._dragObject and self._selectedObj is not None and  not self._selectedObj.isLock():
                for obj in self._environment.getObjects():
                    if self._selectedObj.isCollidedWith(obj) and self._selectedObj!=obj:
                        obj.setCollidedState(False)
                pose = self._selectedObj.getPose()
                pose.move(self._convertedMousePose.x() - self._selectionOffset[0], self._convertedMousePose.y() - self._selectionOffset[1])

                if isinstance(self._selectedObj,Robot):
                    self._selectedObj.deleteTrajectory()

        if self._dragScene:
            current=event.pos()
            Rescaling.setOffset(Rescaling.getOffset()+(current-self._dragSceneOrigin))
            self._dragSceneOrigin=current

    def _isClickedObject(self, mousePose):
        convertedMousePose = (mousePose - Rescaling.getOffset()) / Rescaling.zoom
        for obj in self._environment.getObjects():
            obj.setSelected(False)
            if obj.getRepresentation().contains(convertedMousePose) and obj.isVisible():
                obj.setSelected(True)
                self._selectedObj = obj
                pose = obj.getPose()
                dx = convertedMousePose.x() - pose.getX()
                dy = convertedMousePose.y() - pose.getY()
                self._selectionOffset = (dx, dy)
        if self._selectedObj is not None and not self._selectedObj.isLock():
            self._selectedObj.setCollidedState(True)
        self._explorer.setSelectedItem(self._selectedObj)

    def wheelEvent(self, event):
        if event.modifiers() and Qt.ControlModifier:
            dir=event.angleDelta().y()
            dir/=abs(dir)

            pos1 = (event.pos() - Rescaling.getOffset()) / Rescaling.zoom

            Rescaling.zoomIn() if dir>0 else Rescaling.zoomOut()
            # self._footer.setZoom()

            s = ((self._size - self._size * Rescaling.zoom) / 2)
            offset = QPoint(s.width(), s.height()) # pour centrer la fenêtre
            pos2 = (event.pos() - offset) / Rescaling.zoom
            # pos1 doit devenir pos1 transformée dans le nouveau zoom
            getEqualCoordinatesOffset = (pos1-pos2)*Rescaling.zoom
            Rescaling.setOffset(offset-getEqualCoordinatesOffset)

    def maximized(self):
        self._maximized=True

    def resizeEvent(self,event):
        if self._maximized and self._size is None:
            self._size=self.size()
            Rescaling.sceneSize = self._size
            if not self._environment.hasSize():
                self._environment.setSize(self._size)
            Rescaling.zoomToMiniFit()
            self._environment.drawWalls()

