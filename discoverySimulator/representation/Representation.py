from .shapes import Shape

class Representation:
    def __init__(self,shape):
        """
        This method allows to add a representation of an object
        :param shape: shape of the object
        """
        self._shape=None
        self.setShape(shape)
        self._subRepresentations=[]
        self._pose=None
        self._visible = True

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

    def setVisible(self,visible):
        self._visible = visible

    def toggleVisible(self):
        self._visible=not self._visible

    def isVisible(self):
        return self._visible

    def paint(self,painter):
        if self._visible:
            self._shape.paint(painter)
            for rep in self._subRepresentations:
                painter.save() # sauvegarde de l'état du painter
                rep.paint(painter)
                painter.restore() # restoration de l'état du painter

    def contains(self,point):
        return self._shape.contains(point)
