from robotSimulator.Shape import Shape
from robotSimulator.Point import Point

class Representation:
    def __init__(self,shape):
        self._representation=None
        self.setRepresentation(shape)
        self._subRepresentations=[]
        self._center=Point(0,0)
        self._orientation=0

    def setParameters(self,center,orientation):
        self._center = center
        self._orientation=orientation

    def getCenter(self):
        return self._center

    def getOrientation(self):
        return self._orientation

    def getRepresentation(self):
        return self._representation

    def addSubRepresentation(self,rep):
        if isinstance(rep,Representation):
            self._subRepresentations.append(rep)

    def setRepresentation(self,shape):
        if isinstance(shape,Shape):
            self._representation=shape

    def paint(self,painter):
        self._representation.paint(painter,self._center,self._orientation)
        for rep in self._subRepresentations:
            painter.save() # sauvegarde de l'état du painter
            rep.paint(painter)
            painter.restore() # restoration de l'état du painter