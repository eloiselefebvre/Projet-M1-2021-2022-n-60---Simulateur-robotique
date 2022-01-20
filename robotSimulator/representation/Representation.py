from robotSimulator.representation.shapes.Shape import Shape
from robotSimulator.representation.shapes.Point import Point

class Representation:
    def __init__(self,shape):
        self._representation=None
        self.setRepresentation(shape)
        self._subRepresentations=[]
        self._origin=Point(0,0)
        self._orientation=0

    def setParameters(self,origin,orientation):
        self._origin = origin
        self._orientation=orientation

    def getRepresentation(self):
        return self._representation

    def addSubRepresentation(self,rep):
        if isinstance(rep,Representation):
            self._subRepresentations.append(rep)

    def setRepresentation(self,shape):
        if isinstance(shape,Shape):
            self._representation=shape

    def paint(self,painter):
        self._representation.paint(painter,self._origin,self._orientation)
        for rep in self._subRepresentations:
            painter.save() # sauvegarde de l'état du painter
            rep.paint(painter)
            painter.restore() # restoration de l'état du painter