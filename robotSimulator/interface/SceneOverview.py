from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget
from robotSimulator.Rescaling import Rescaling

class SceneOverview(QWidget):

    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self.setStyleSheet("background-color: #f0f0f0")

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.scale(Rescaling.miniZoom, Rescaling.miniZoom)
        for obj in self._environment.getObjects():
            painter.save()
            obj.paint(painter)
            painter.restore()

        for obj in self._environment.getVirtualObjects():
            painter.save()
            obj.paint(painter)
            painter.restore()

        painter.setPen(QPen(QColor("#675BB5"),8, Qt.SolidLine))

        ox=-int(Rescaling.offsetX/Rescaling.zoom)
        oy=-int(Rescaling.offsetY/Rescaling.zoom)
        w=int(Rescaling.sceneSize.width()/Rescaling.zoom)
        h=int(Rescaling.sceneSize.height()/Rescaling.zoom)

        painter.drawRect(ox,oy,ox+w,oy+h)
