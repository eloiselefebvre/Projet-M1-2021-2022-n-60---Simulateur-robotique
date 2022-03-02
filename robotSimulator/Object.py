from PyQt5.QtGui import QPainter

from robotSimulator.representation.shapes import Border
from robotSimulator.Rescaling import Rescaling

class Object:

    SELECTED_COLOR = "#25CCF7"
    NUMBER_OF_INSTANCES = {}

    # TODO : Gestion des ID des sensors dans l'environnement

    def __init__(self,representation):
        self._pose = None
        self._representation = representation
        self._env= None
        self._collided = False
        self._lock=False
        self.setNumberOfInstances(type(self).__name__)
        self._id = type(self).__name__
        self.completeID()

    def setNumberOfInstances(self,name):
        if name in self.NUMBER_OF_INSTANCES:
            Object.NUMBER_OF_INSTANCES[name]+=1
        else:
            Object.NUMBER_OF_INSTANCES[name]=1

    def getRepresentation(self):
        return self._representation

    def paint(self, painter):
        self._representation.paint(painter)

    def setPose(self,pose):
        self._pose=pose
        self._representation.setPose(self._pose)

    def getPose(self):
        return self._pose

    def getID(self):
        return self._id

    def isLock(self):
        return self._lock

    def setLock(self,lock):
        self._lock=lock

    def toggleLock(self):
        self._lock=not self._lock

    def isVisible(self):
        return self._representation.isVisible()

    def setVisible(self, visible):
        self._representation.setVisible(visible)

    def toggleVisible(self):
        self._representation.toggleVisible()

    def setID(self,id):
        self._id=id
        Object.NUMBER_OF_INSTANCES[type(self).__name__] -= 1
        self.setNumberOfInstances(self._id)
        self.completeID()

    def completeID(self):
        self._id+="_"+str(Object.NUMBER_OF_INSTANCES[self._id])

    def setSelected(self,selected):
        if selected:
            self._representation.getShape().addBorder(Border(4, self.SELECTED_COLOR))
        else:
            self._representation.getShape().removeBorder()

    def setEnv(self,env):
        self._env=env

    def getEnv(self):
        return self._env

    def getCollidedState(self):
        return self._collided

    def setCollidedState(self,state):
        self._collided=state

    def isCollided(self):
        if not self._collided:
            for obj in self._env.getObjects():
                if self!=obj and self.isCollidedWith(obj):
                    self._collided=True
                    obj.setCollidedState(True)

    # MSO TODO : attention, par convention, les méthodes isXXX() renvoient des booléens. J'ai l'impression qu'ici, on renvoie des intersections. Nom à revoir
    def isCollidedWith(self,obj):
        return self.getRepresentation().getShape().isCollidedWith(obj.getRepresentation().getShape())



