from discoverySimulator.Observable import Observable
from PyQt5.QtCore import QPoint, QSize


class ZoomController(Observable):

    __ZOOM_STEP = 0.1
    __ZOOM_MIN = 0.1
    __ZOOM_MAX  = 3.0

    def __init__(self,environnement):
        super().__init__()
        self.__environnementSize = environnement.getSize()
        self.__sceneSize = None
        self.__sceneOverviewSize = None

        self.__zoom=1.0
        self.__overviewZoom=1.0

        self.__offset=QPoint(0, 0)
        self.__overviewOffset=QPoint(0, 0)

    def setZoom(self, zoom:float):
        if zoom >= ZoomController.__ZOOM_MIN and zoom <= ZoomController.__ZOOM_MAX:
            self.__zoom = zoom
            self.zoomChanged()
            return True
        if zoom > self.__ZOOM_MAX:
            self.__zoom = ZoomController.__ZOOM_MAX
            self.zoomChanged()
            return True
        return False

    def setSceneSize(self, size:QSize):
        self.__sceneSize = size
        if self.__offset.isNull():
            off = (self.__sceneSize-self.__environnementSize)/2
            if off.width()>0 and off.height()>0:
                self.__offset=QPoint(off.width(),off.height())

    def setSceneOverviewSize(self, size:QSize):
        self.__sceneOverviewSize = size

    def setOffset(self, offset:QPoint):
        self.__offset = offset

    def getZoom(self):
        return self.__zoom

    def getZoomOverview(self):
        return self.__overviewZoom

    def getOffset(self) -> QPoint:
        return self.__offset

    def getOverviewOffset(self) -> QPoint:
        return self.__overviewOffset

    def getSceneSize(self):
        return self.__sceneSize

    def zoomIn(self):
        self.__zoom+=ZoomController.__ZOOM_STEP
        self.__zoom = min(self.__zoom, ZoomController.__ZOOM_MAX)
        self.zoomChanged()

    def zoomOut(self):
        self.__zoom-=ZoomController.__ZOOM_STEP
        self.__zoom = max(self.__zoom, ZoomController.__ZOOM_MIN)
        self.zoomChanged()

    def zoomToFit(self):
        self.__zoom=min(self.__sceneSize.width() / self.__environnementSize.width(), self.__sceneSize.height() / self.__environnementSize.height())
        off = (self.__sceneSize - self.__environnementSize*self.__zoom) / 2
        self.__offset = QPoint(off.width(), off.height())
        self.zoomChanged()

    def zoomOverviewToFit(self):
        self.__overviewZoom=min(self.__sceneOverviewSize.width() / self.__environnementSize.width(), self.__sceneOverviewSize.height() / self.__environnementSize.height())
        off = (self.__sceneOverviewSize - self.__environnementSize * self.__overviewZoom) / 2
        self.__overviewOffset = QPoint(off.width(), off.height())

    def zoomChanged(self):
        self.notifyObservers("zoomChanged")