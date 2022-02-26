from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from robotSimulator.Rescaling import Rescaling

class Scene(QWidget):

    def __init__(self,environment,explorer):
        super().__init__()
        self._environment = environment
        self._explorer=explorer
        self._drag=False
        self._selectedObj = None
        self._selectionOffset=(0,0)
        self._maximized = False
        self._size=None

    def paintEvent(self,event):
        for obj in self._environment.getObjects():
            obj.paint(self)
        for obj in self._environment.getVirtualObjects():
            obj.paint(self)
        self.update()

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self._isClickedObject(event.pos())
            self._drag=True

    def mouseReleaseEvent(self,event):
        self._drag=False
        if self._selectedObj is not None:
            self._selectedObj.setCollidedState(False)
            self._selectedObj = None

    def mouseMoveEvent(self, event):
        if self._drag:
            convertedMousePose = (event.pos() - Rescaling.getOffset()) / Rescaling.zoom
            if self._selectedObj is not None and not self._selectedObj.isLock():
                for obj in self._environment.getObjects():
                    if self._selectedObj.isCollidedWith(obj) and self._selectedObj!=obj:
                        obj.setCollidedState(False)
                pose = self._selectedObj.getPose()
                pose.move(convertedMousePose.x()-self._selectionOffset[0],convertedMousePose.y()-self._selectionOffset[1])

    def _isClickedObject(self, mousePose):
        convertedMousePose = (mousePose - Rescaling.getOffset()) / Rescaling.zoom
        for obj in self._environment.getObjects():
            obj.setSelected(False)
            if obj.getRepresentation().contains(convertedMousePose) and obj.isVisible():  # contains mousePose
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
        # TODO : Faire le zoom sur le curseur
        dir=event.angleDelta().y()
        dir/=abs(dir)
        # pz=Rescaling.zoom
        if dir>0:
            Rescaling.zoomIn()
        else:
            Rescaling.zoomOut()
        # if Rescaling.zoom!=Rescaling.min_zoom and Rescaling.zoom!=Rescaling.max_zoom:
        #     s=((self._size-self._size*Rescaling.zoom)/2)
        #     offset = QPoint(s.width(),s.height())
        #     print("\nreal",event.pos()-QPoint(int(500*Rescaling.zoom),int(500*Rescaling.zoom)))
        #     print(500*Rescaling.zoom,event.pos(),event.pos()-((event.pos()-Rescaling.getOffset())+dir*event.pos()*Rescaling.dzoom),((event.pos()-Rescaling.getOffset())+dir*event.pos()*Rescaling.dzoom))
        #     #Rescaling.setOffset(event.pos()-QPoint(int(500*Rescaling.zoom),int(500*Rescaling.zoom)))
        #     Rescaling.setOffset(event.pos()-((event.pos()-Rescaling.getOffset())+dir*event.pos()*Rescaling.dzoom))
        #     #Rescaling.setAfterOffset()
        # if Rescaling.zoom==1:
        #     Rescaling.setAfterOffset(QPoint(0,0))
        s = ((self._size - self._size * Rescaling.zoom) / 2)
        offset = QPoint(s.width(), s.height())
        Rescaling.setOffset(offset)

    def maximized(self):
        self._maximized=True

    def resizeEvent(self,event):
        if self._maximized and self._size is None:
            self._size=self.size()
            self._environment.drawWalls(self.width(),self.height())

