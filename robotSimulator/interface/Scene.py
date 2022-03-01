from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from robotSimulator.Rescaling import Rescaling

class Scene(QWidget):

    def __init__(self,environment,explorer,footer):
        super().__init__()
        self._environment = environment
        self._explorer=explorer
        self._footer=footer
        self._dragObject=False
        self._dragScene = False
        self._dragSceneOrigin=QPoint(0,0)
        self._selectedObj = None
        self._selectionOffset=(0,0)
        self._maximized = False
        self._size=None
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)

    def paintEvent(self,event):
        for obj in self._environment.getObjects():
            obj.paint(self)
        for obj in self._environment.getVirtualObjects():
            obj.paint(self)
        self.update()

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

    def mouseMoveEvent(self, event):
        convertedMousePose = (event.pos() - Rescaling.getOffset()) / Rescaling.zoom
        self._footer.setMousePose(convertedMousePose)
        if self._dragObject:
            if self._selectedObj is not None and not self._selectedObj.isLock():
                for obj in self._environment.getObjects():
                    if self._selectedObj.isCollidedWith(obj) and self._selectedObj!=obj:
                        obj.setCollidedState(False)
                pose = self._selectedObj.getPose()
                pose.move(convertedMousePose.x()-self._selectionOffset[0],convertedMousePose.y()-self._selectionOffset[1])

        if self._dragScene:
            current=event.pos()
            Rescaling.setOffset(Rescaling.getOffset()+(current-self._dragSceneOrigin))
            self._dragSceneOrigin=current

    def _isClickedObject(self, mousePose):
        # TODO : Ne pas arrêter le robot s'il est verrouillé
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
        if self._selectedObj is not None:
            self._selectedObj.setCollidedState(True)
        self._explorer.setSelectedItem(self._selectedObj)

    def wheelEvent(self, event):
        if event.modifiers() and Qt.ControlModifier:
            dir=event.angleDelta().y()
            dir/=abs(dir)

            pos1 = (event.pos() - Rescaling.getOffset()) / Rescaling.zoom

            Rescaling.zoomIn() if dir>0 else Rescaling.zoomOut()
            self._footer.setZoom()

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
            self._environment.drawWalls(self.width(),self.height())

