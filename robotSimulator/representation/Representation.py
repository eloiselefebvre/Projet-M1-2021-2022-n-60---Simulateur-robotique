from .shapes import Shape
from robotSimulator import Point


class Representation:
    def __init__(self,shape):
        self._representation=None
        self.setRepresentation(shape)
        self._subRepresentations=[]
        self._pose=None

    def setPose(self,pose):
        self._pose=pose

    def getRepresentation(self):
        return self._representation

    def addSubRepresentation(self,rep):
        if isinstance(rep,Representation):
            self._subRepresentations.append(rep)

    def setRepresentation(self,shape):
        if isinstance(shape,Shape):
            self._representation=shape

    def paint(self,painter):
        self._representation.paint(painter,self._pose)
        for rep in self._subRepresentations:
            painter.save() # sauvegarde de l'état du painter
            rep.paint(painter)
            painter.restore() # restoration de l'état du painter