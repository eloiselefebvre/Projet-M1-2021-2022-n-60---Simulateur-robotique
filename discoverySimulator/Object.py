from typing import List

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter

from discoverySimulator.Pose import Pose
from discoverySimulator.Frame import Frame
from discoverySimulator.Observable import Observable
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Border import Border


class Object(Observable):

    SELECTED_COLOR = "#25CCF7"
    number_of_instances = {}

    def __init__(self,representation):
        """
        This method allows to create a new object
        :param representation: representation of the object
        """
        super().__init__()
        self._pose = None
        self._representation = representation
        self._environnement= None
        self._isCollided = False
        self._isSelected = False
        self._acceleration = 1  # TODO : Revoir le changement lorsque l'accelaration est initialement définie et meilleure façon de partager des variables à plusieurs entités
        self._visibilityLocked = False
        self._zIndex = 1
        self._frame=Frame()
        self.setNumberOfInstances(type(self).__name__)
        self._id = type(self).__name__
        self.completeID()

    # SETTERS
    def setFrame(self,frame:Frame):
        if isinstance(frame,Frame):
            self._frame=frame

    def setZIndex(self,index:int):
        self._zIndex=int(index)

    def setNumberOfInstances(self,name:str):
        """
        This method is used to count the number of instances of an object
        :param name: name of the object
        """
        if name in self.number_of_instances:
            Object.number_of_instances[name]+=1
        else:
            Object.number_of_instances[name]=1

    def setPose(self,pose:Pose):
        self._pose=pose
        self._representation.setPose(self._pose)

    def setVisible(self, visible:bool):
        if not self._visibilityLocked:
            self._representation.setVisible(visible)
            self.visibylityChanged()

    def setVisibilityLocked(self,state:bool):
        self._visibilityLocked=state

    def setID(self,id:str):
        """
        This method is used to change the ID of an object
        :param id: new id of the object
        """
        self._id=id
        Object.number_of_instances[type(self).__name__] -= 1
        self.setNumberOfInstances(self._id)
        self.completeID()

    def setSelected(self,selected:bool):
        if selected!=self._isSelected:
            self._isSelected=selected
            if self._isSelected:
                self._representation.getShape().addBorder(Border(4, self.SELECTED_COLOR))
            else:
                self._representation.getShape().removeBorder()
            self.notifyObservers("selectionChanged")

    def setCollidedState(self,state):
        self._isCollided=state

    def setEnvironnement(self, environnement):
        self._environnement=environnement

    # GETTERS
    def getFrame(self) -> Frame:
        return self._frame

    def getAcceleration(self) -> float:
        return self._acceleration

    def getZIndex(self) -> int:
        return self._zIndex

    def getRepresentation(self) -> Representation:
        """
        This method is used to get the representation of an object
        :return: the representation of the object
        """
        return self._representation

    def getPose(self) -> Pose:
        return self._pose

    def getID(self) -> str:
        """
        This method is used to get the ID of an object
        :return: the ID of the object
        """
        return self._id

    def getVisibilityLocked(self) -> bool:
        return self._visibilityLocked

    def getEnvironnement(self) :
        return self._environnement

    def getCollidedState(self) -> bool:
        return self._isCollided

    def getIntersectionsWith(self,obj) -> List[QPointF]:
        return self.getRepresentation().getShape().getIntersectionsWith(obj.getRepresentation().getShape())

    def paint(self, painter:QPainter):
        self._representation.paint(painter)

    def isVisible(self) -> bool:
        return self._representation.isVisible()

    def toggleVisible(self):
        if not self._visibilityLocked:
            self._representation.toggleVisible()
            self.visibylityChanged()

    def visibylityChanged(self):
        if hasattr(self,'getComponents'):
            for comp in self.getComponents():
                comp.setVisibilityLocked(not self.isVisible())
        self.notifyObservers("visibilityChanged")

    def completeID(self):
        self._id+="_"+str(Object.number_of_instances[self._id])

    def isSelected(self) -> bool:
        return self._isSelected

    def isCollided(self):
        if not self._isCollided:
            for obj in self._environnement.getObjects():
                if self!=obj and self.isCollidedWith(obj):
                    self._isCollided=True
                    obj.setCollidedState(True)

    def isCollidedWith(self,obj) -> bool:
        return len(self.getIntersectionsWith(obj))!=0

    def accelerationChanged(self,sender):
        self._acceleration=sender.getAcceleration()