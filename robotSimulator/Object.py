from robotSimulator.Frame import Frame
from robotSimulator.Observable import Observable
from robotSimulator.representation.shapes.Border import Border

class Object(Observable):

    SELECTED_COLOR = "#25CCF7"
    number_of_instances = {}

    def __init__(self,representation):
        super().__init__()
        self._pose = None
        self._representation = representation
        self._env= None
        self._isCollided = False
        self._isSelected = False

        self._acceleration = 1  # TODO : Revoir le changement lorsque l'accelaration est initialement définie et meilleure façon de partager des variables à plusieurs entités

        self._visibilityLocked = False

        self._z_index = 1

        self._frame=Frame()

        self.setNumberOfInstances(type(self).__name__)
        self._id = type(self).__name__
        self.completeID()

        # TODO : Handle all visible variables here and not in representation

    def setFrame(self,frame):
        if isinstance(frame,Frame):
            self._frame=frame

    def getFrame(self):
        return self._frame

    def setZIndex(self,index):
        self._z_index=index

    def getZIndex(self):
        return self._z_index

    def setNumberOfInstances(self,name):
        if name in self.number_of_instances:
            Object.number_of_instances[name]+=1
        else:
            Object.number_of_instances[name]=1

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

    def isVisible(self):
        return self._representation.isVisible()

    def setVisible(self, visible):
        if not self._visibilityLocked:
            self._representation.setVisible(visible)
            self.visibylityChanged()

    def toggleVisible(self):
        if not self._visibilityLocked:
            self._representation.toggleVisible()
            self.visibylityChanged()

    def visibylityChanged(self):
        if hasattr(self,'getComponents'):
            for comp in self.getComponents():
                comp.setVisibilityLocked(not self.isVisible())
        self.notifyObservers("visibilityChanged")

    def setVisibilityLocked(self,state):
        self._visibilityLocked=state

    def getVisibilityLocked(self):
        return self._visibilityLocked

    def setID(self,id):
        self._id=id
        Object.number_of_instances[type(self).__name__] -= 1
        self.setNumberOfInstances(self._id)
        self.completeID()

    def completeID(self):
        self._id+="_"+str(Object.number_of_instances[self._id])

    def setSelected(self,selected):
        if selected!=self._isSelected:
            self._isSelected=selected
            if self._isSelected:
                self._representation.getShape().addBorder(Border(4, self.SELECTED_COLOR))
            else:
                self._representation.getShape().removeBorder()
            self.notifyObservers("selectionChanged")

    def isSelected(self):
        return self._isSelected

    def setEnv(self,env):
        self._env=env

    def getEnv(self):
        return self._env

    def getCollidedState(self):
        return self._isCollided

    def setCollidedState(self,state):
        self._isCollided=state

    def isCollided(self):
        if not self._isCollided:
            for obj in self._env.getObjects():
                if self!=obj and self.isCollidedWith(obj):
                    self._isCollided=True
                    obj.setCollidedState(True)

    # MSO TODO : attention, par convention, les méthodes isXXX() renvoient des booléens. J'ai l'impression qu'ici, on renvoie des intersections. Nom à revoir
    def isCollidedWith(self,obj):
        return self.getRepresentation().getShape().isCollidedWith(obj.getRepresentation().getShape())

    def getAcceleration(self):
        return self._acceleration

    def accelerationChanged(self,sender):
        self._acceleration=sender.getAcceleration()