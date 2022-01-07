from abc import abstractmethod

class Representation:

    def __init__(self,origin,orientation,color):
        super().__init__()
        self._origin = origin
        self._color = color
        self._orientation=orientation

    def print(self):
        print("Shape - origin :",self._origin)

    @abstractmethod
    def draw(self,painter):
        pass

