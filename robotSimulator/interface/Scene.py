from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint

from robotSimulator.Observable import Observable
from robotSimulator.robots.Robot import Robot


class Scene(QWidget,Observable):

    def __init__(self,environment,zoomController):
        super().__init__()
        self._environment = environment

        self._zoomController = zoomController
        self._explorer=None
        self._dragObject=False
        self._isSceneLocked=False
        self._dragScene = False
        self._dragSceneOrigin=QPoint(0,0)

        self._selectionOffset=(0,0)
        self._maximized = False
        self._size=None
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)

        self._selectedObj = None
        self._objectMoved=False

        self.setStyleSheet("background-color: #f0f0f0")

        self._convertedMousePose=QPoint(0, 0)

    def defineExplorer(self,explorer):
        self._explorer=explorer

    def refreshView(self,sender):
        self.update()

    def updateLockedScene(self,sender):
        self._isSceneLocked=sender.getLockState()

    def paintEvent(self,event):
        painter = QPainter(self)
        offset=self._zoomController.getOffset()
        painter.translate(offset.x(), offset.y())
        painter.scale(self._zoomController.getZoom(),self._zoomController.getZoom())

        for obj in self._environment.getVirtualObjects():
            painter.save()
            obj.paint(painter)
            painter.restore()

        for obj in self._environment.getObjects():
            painter.save()
            obj.paint(painter)
            painter.restore()


    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        if event.button()==Qt.LeftButton:
            self._objectGrabbed(event.pos())
            self._dragObject=True

        if event.button() == Qt.MiddleButton:
            self._dragScene = True
            self._dragSceneOrigin = event.pos()

    def mouseReleaseEvent(self,event):
        self.setCursor(Qt.OpenHandCursor)
        self._dragObject=False
        self._dragScene=False
        if self._selectedObj is not None:
            if self._objectMoved:
                self._objectMoved=False
                self._selectedObj.setCollidedState(False)
            self._selectedObj=None

    def mousePose(self):
        return self._convertedMousePose

    def mouseMoveEvent(self, event):
        self._convertedMousePose = (event.pos() -  self._zoomController.getOffset()) /  self._zoomController.getZoom()
        self.notifyObservers("poseChanged")
        if self._dragObject and self._selectedObj is not None:
            for obj in self._environment.getObjects():
                if self._selectedObj.isCollidedWith(obj) and self._selectedObj!=obj:
                    obj.setCollidedState(False)
            pose = self._selectedObj.getPose()
            pose.move(self._convertedMousePose.x() - self._selectionOffset[0], self._convertedMousePose.y() - self._selectionOffset[1])
            self._objectMoved=True
            if isinstance(self._selectedObj,Robot):
                self._selectedObj.deleteTrajectory()

            self._selectedObj.notifyObservers("poseChanged") # TODO : notify directement dans une méthode move de l'objet

        if self._dragScene:
            current=event.pos()
            self._zoomController.setOffset(self._zoomController.getOffset()+(current-self._dragSceneOrigin))
            self._dragSceneOrigin=current

    def _objectGrabbed(self, mousePose):
        convertedMousePose = (mousePose - self._zoomController.getOffset()) / self._zoomController.getZoom()
        for obj in self._environment.getObjects():
            obj.setSelected(False)

        for obj in self._environment.getObjects():
            if obj.getRepresentation().contains(convertedMousePose) and obj.isVisible():
                obj.setSelected(True)
                pose = obj.getPose()
                dx = convertedMousePose.x() - pose.getX()
                dy = convertedMousePose.y() - pose.getY()
                self._selectionOffset = (dx, dy)
                if not self._isSceneLocked:
                    self._selectedObj = obj
                    self._selectedObj.setCollidedState(True)


    def wheelEvent(self, event):
        if event.modifiers() and Qt.ControlModifier:
            dir=event.angleDelta().y()
            dir/=abs(dir)

            pos1 = (event.pos() - self._zoomController.getOffset()) / self._zoomController.getZoom()

            self._zoomController.zoomIn() if dir>0 else self._zoomController.zoomOut()

            s = ((self._size - self._size * self._zoomController.getZoom()) / 2)
            offset = QPoint(s.width(), s.height()) # pour centrer la fenêtre
            pos2 = (event.pos() - offset) / self._zoomController.getZoom()
            # pos1 doit devenir pos1 transformée dans le nouveau zoom
            getEqualCoordinatesOffset = (pos1-pos2)*self._zoomController.getZoom()
            self._zoomController.setOffset(offset-getEqualCoordinatesOffset)

    def maximized(self):
        self._maximized=True

    def resizeEvent(self,event):
        if self._maximized:
            self._size=self.size()
            self._zoomController.setSceneSize(self._size)

