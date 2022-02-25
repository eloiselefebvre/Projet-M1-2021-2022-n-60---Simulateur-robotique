from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class Scene(QWidget):

    def __init__(self,environment,explorer):
        super().__init__()
        self._environment = environment
        self._explorer=explorer
        self._drag=False
        self._selectedObj = None
        self._selectionOffset=(0,0)
        self._maximized = False
        self._initialSize = None

    def paintEvent(self,event):
        for obj in self._environment.getObjects():
            obj.paint(self)
        for obj in self._environment.getVirtualObjects():
            obj.paint(self)
        self.update()

    def mousePressEvent(self, event):
        self._drag=False
        if event.button()==Qt.LeftButton:
            self._isClickedObject(event.pos())
            self._drag=True

    def mouseMoveEvent(self, event):
        if self._drag:
            if self._selectedObj is not None and not self._selectedObj.isLock():
                for obj in self._environment.getObjects():
                    if self._selectedObj.isCollidedWith(obj):
                        obj.setCollidedState(False)
                pose = self._selectedObj.getPose()
                pose.move(event.x()-self._selectionOffset[0],event.y()-self._selectionOffset[1])

    def _isClickedObject(self,mousePose):
        self._selectedObj=None
        for obj in self._environment.getObjects():
            obj.setSelected(False)
            if obj.getRepresentation().contains(mousePose) and obj.getRepresentation().isVisible():
                obj.setSelected(True)
                self._selectedObj=obj
                pose=obj.getPose()
                dx = mousePose.x() - pose.getX()
                dy = mousePose.y() - pose.getY()
                self._selectionOffset=(dx,dy)
        self._explorer.setSelectedItem(self._selectedObj)

    def maximized(self):
        self._maximized=True

    def resizeEvent(self,event):
        if self._maximized:
            self._environment.drawWalls(self.width(),self.height())



