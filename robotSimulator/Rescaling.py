from PyQt5.QtCore import QPoint


class Rescaling:

    zoom = 1.0
    min_zoom=0.1
    max_zoom=3.0

    offsetX = 0
    offsetY = 0

    dzoom = 0.1

    sceneSize=None
    envSize=None

    @staticmethod
    def zoomIn():
        Rescaling.zoom+=Rescaling.dzoom
        Rescaling.zoom = min(Rescaling.zoom, Rescaling.max_zoom)

    @staticmethod
    def zoomOut():
        Rescaling.zoom-=Rescaling.dzoom
        Rescaling.zoom = max(Rescaling.zoom, Rescaling.min_zoom)

    @staticmethod
    def zoomToFit():
        print(Rescaling.sceneSize,Rescaling.envSize)
        Rescaling.zoom=min(Rescaling.sceneSize.width()/Rescaling.envSize.width(),Rescaling.sceneSize.height()/Rescaling.envSize.height())
        Rescaling.offsetX=0
        Rescaling.offsetY=0

    @staticmethod
    def setZoom(zoom):
        if zoom>=Rescaling.min_zoom and zoom<=Rescaling.max_zoom:
            Rescaling.zoom=zoom
            return True
        if zoom>Rescaling.max_zoom:
            Rescaling.zoom=Rescaling.max_zoom
            return True
        return False

    @staticmethod
    def setOffset(offset):
        Rescaling.offsetX=offset.x()
        Rescaling.offsetY=offset.y()

    @staticmethod
    def getOffset():
        return QPoint(Rescaling.offsetX,Rescaling.offsetY)