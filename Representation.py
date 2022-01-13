from Shape import Shape

class Representation:
    def __init__(self,shape):
        self._representation=None
        self.setRepresentation(shape)
        self._subRepresentations=[]
        self._posX=0
        self._posY=0
        self._orientation=0

    def setParameters(self,posX,posY,orientation):
        self._posX=posX
        self._posY=posY
        self._orientation=orientation

    def getPosX(self):
        return self._posX

    def getPosY(self):
        return self._posY

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
        self._representation.paint(painter,self._posX,self._posY,self._orientation)
        for rep in self._subRepresentations:
            painter.save() # sauvegarde de l'état du painter
            rep.getRepresentation().paint(painter,rep.getPosX(),rep.getPosY(),rep.getOrientation())
            painter.restore() # restoration de l'état du painter