from discoverySimulator.Observable import Observable
from PyQt5.QtCore import QPoint


class ZoomController(Observable):

    ZOOM_STEP = 0.1
    ZOOM_MIN = 0.1
    ZOOM_MAX  = 3.0

    def __init__(self,environnement):
        super().__init__()
        self._envSize = environnement.getSize()
        self._sceneSize = None
        self._miniSceneSize = None

        self._zoom=1.0
        self._miniZoom=1.0

        self._offset=QPoint(0,0) # TODO : utiliser Point qui hériterait de QPoint?

    def zoomIn(self):
        self._zoom+=self.ZOOM_STEP
        self._zoom = min(self._zoom,self.ZOOM_MAX)
        self.zoomChanged()

    def zoomOut(self):
        self._zoom-=self.ZOOM_STEP
        self._zoom = max(self._zoom,self.ZOOM_MIN)
        self.zoomChanged()

    def zoomToFit(self):
        self._zoom=min(self._sceneSize.width()/self._envSize.width(),self._sceneSize.height()/self._envSize.height())
        self._offset=QPoint(0,0)
        self.zoomChanged()

    def zoomToMiniFit(self):
        self._miniZoom=min(self._miniSceneSize.width()/self._envSize.width(),self._miniSceneSize.height()/self._envSize.height())

    def setZoom(self,zoom):
        if zoom>=self.ZOOM_MIN and zoom<=self.ZOOM_MAX:
            self._zoom=zoom
            self.zoomChanged()
            return True
        if zoom>self.ZOOM_MAX:
            self._zoom=self.ZOOM_MAX
            self.zoomChanged()
            return True
        return False

    def getZoom(self):
        return self._zoom

    def getMiniZoom(self):
        return self._miniZoom

    def setOffset(self,offset):
        self._offset=offset

    def getOffset(self):
        return self._offset

    def setSceneSize(self,size):
        self._sceneSize=size

    def getSceneSize(self):
        return self._sceneSize

    def setMiniSceneSize(self,size):
        self._miniSceneSize=size

    def zoomChanged(self):
        self.notifyObservers("zoomChanged")