from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget


class Explorer(QWidget):

    def __init__(self,environment):
        super(Explorer, self).__init__()
        self._environment = environment

        #juste pour visualiser
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#333333'))
        self.setPalette(palette)

    def printObjects(self):
        text=""
        for obj in self._environment.getObjects():
            text+=str(obj)+"\n"
        return(text)








