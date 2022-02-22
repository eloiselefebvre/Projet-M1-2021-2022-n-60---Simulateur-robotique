from PyQt5.QtWidgets import QWidget


class Scene(QWidget):

    def __init__(self,environment):
        super().__init__()
        self._environment = environment

    def paintEvent(self,event):
        for obj in self._environment.getObjects():
            # MSO TODO : ne pas mettre la fenêtre dans paint(), mais plutôt le widget qui correspond à la zone de dessin (Panel principal) -- vous aurez beaucoup d'autres composants par la suite
            obj.paint(self)
        self.update()



