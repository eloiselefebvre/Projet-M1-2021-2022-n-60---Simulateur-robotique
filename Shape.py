class Shape:
    def __init__(self,color,opacity,borderWidth,borderColor):
        self._color = color # QColor de color
        self._opacity=opacity
        self._borderWidth=borderWidth
        self._borderColor=color if borderColor is None else borderColor

    def paint(self,painter,x,y,orientation):
        pass

    def setOpacity(self,opacity):
        self._opacity=opacity