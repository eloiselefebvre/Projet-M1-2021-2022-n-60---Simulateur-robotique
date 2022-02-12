from .shapes import Shape
from robotSimulator import Point

class Representation:
    def __init__(self,shape):
        self._shape=None
        self.setShape(shape)
        self._subRepresentations=[]
        self._pose=None

    def getShape(self):
        return self._shape

    def setPose(self,pose):
        self._pose=pose
        self._shape.setPose(self._pose)

    def addSubRepresentation(self,rep):
        if isinstance(rep,Representation):
            self._subRepresentations.append(rep)

    def setShape(self,shape):
        if isinstance(shape,Shape):
            self._shape=shape

    def paint(self,painter):
        self._shape.paint(painter)
        for rep in self._subRepresentations:
            painter.save() # sauvegarde de l'état du painter
            rep.paint(painter)
            painter.restore() # restoration de l'état du painter