from PyQt5.QtCore import QPoint


class Rescaling:

    zoom = 1.0
    min_zoom=0.1
    max_zoom=1.0
    offsetX = 0
    offsetY = 0
    innerOffset=QPoint(0,0)

    dzoom = 0.1

    @staticmethod
    def setZoom(zoom):
        Rescaling.zoom=zoom

    @staticmethod
    def zoomIn():
        Rescaling.zoom+=Rescaling.dzoom
        Rescaling.zoom = min(Rescaling.zoom, Rescaling.max_zoom)

    @staticmethod
    def zoomOut():
        Rescaling.zoom-=Rescaling.dzoom
        Rescaling.zoom = max(Rescaling.zoom, Rescaling.min_zoom)

    @staticmethod
    def scaleValue(value):
        return Rescaling.zoom*value

    @staticmethod
    def setOffset(offset):
        # scaleOffset = offset/Rescaling.zoom
        # Rescaling.offsetX=scaleOffset.x()-offset.x()
        # Rescaling.offsetY=scaleOffset.y()-offset.y()
        Rescaling.offsetX=offset.x()
        Rescaling.offsetY=offset.y()

    @staticmethod
    def setInnerOffset(offset):
        Rescaling.innerOffset=offset

    @staticmethod
    def getInnerOffset():
        return Rescaling.innerOffset

    @staticmethod
    def getOffset():
        return QPoint(Rescaling.offsetX,Rescaling.offsetY)