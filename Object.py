class Object:

    def __init__(self,width,height,x,y,orientation,representation):
        self._width = width
        self._height = height
        self._x = x
        self._y = y
        self._orientation = orientation
        self._representation = representation

    def draw(self,window):
        self._representation.draw(window)

