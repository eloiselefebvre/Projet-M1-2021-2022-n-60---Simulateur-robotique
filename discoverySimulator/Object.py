from typing import List

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter

from discoverySimulator.Pose import Pose
from discoverySimulator.Frame import Frame
from discoverySimulator.Observable import Observable
from discoverySimulator.config import colors
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Border import Border


class Object(Observable):

    """ The Object class provides ...."""

    __number_of_instances = {}

    def __init__(self,representation):
        """ This method allows to create a new object
        @param representation  Representation of the object
        """
        super().__init__()
        self._pose = None
        self._representation = representation
        self._environment= None
        self._isCollided = False
        self._isSelected = False
        self._acceleration = 1  # TODO : Revoir le changement lorsque l'accelaration est initialement définie et meilleure façon de partager des variables à plusieurs entités
        self._visibilityLocked = False
        self._zIndex = 1
        self._frame=Frame()
        self._id = type(self).__name__.replace('Rectangular','').replace('Circular','')
        self.setNumberOfInstances(self._id)
        self.completeID()

    # SETTERS
    def setFrame(self,frame:Frame):
        if isinstance(frame,Frame):
            self._frame=frame

    def setZIndex(self,index:int):
        """ This method is used to change the Z index of an object
        @param index  New Z index of the object
        """
        self._zIndex=int(index)

    def setNumberOfInstances(self,name:str):
        """ This method is used to count the number of instances of an object
        @param name  Name of the object
        """
        if name in self.__number_of_instances:
            Object.__number_of_instances[name]+=1
        else:
            Object.__number_of_instances[name]=1

    def setPose(self,pose:Pose):
        """ This method is used to change the position and the orientation of an object
        @param pose New position and orientation of the object
        """
        self._pose=pose
        self._representation.setPose(self._pose)

    def setVisible(self, visible:bool):
        """ This method is used to change the visibility of an object
        @param visible  If the object will be visible or not
        """
        if not self._visibilityLocked:
            self._representation.setVisible(visible)
            self.visibylityChanged()

    def setVisibilityLocked(self,state:bool):
        """ This method is used to change if the visibility of an object is locked or not
        @param state  If the visibility is locked
        """
        self._visibilityLocked=state

    def setID(self,id:str):
        """ This method is used to change the ID of an object
        @param id  New id of the object
        """
        Object.__number_of_instances[self._id.split("_")[0]] -= 1
        self._id=id
        self.setNumberOfInstances(self._id)
        self.completeID()

    def setSelected(self,selected:bool):
        if selected!=self._isSelected:
            self._isSelected=selected
            if self._isSelected:
                self._representation.getShape().addBorder(Border(4, colors['borderColor']))
            else:
                self._representation.getShape().removeBorder()
            self.notifyObservers("selectionChanged")

    def setCollidedState(self,state):
        self._isCollided=state

    def setEnvironnement(self, environnement):
        """ This method allows to set the environment of an object
        @param environnement  The environment of the object
        """
        self._environment=environnement

    # GETTERS
    def getFrame(self) -> Frame:
        return self._frame

    def getAcceleration(self) -> float:
        """ This method is used to get the acceleration of an object
        @return  The acceleration of the object
        """
        return self._acceleration

    def getZIndex(self) -> int:
        """ This method is used to get the Z index of an object
        @return  Z index of the object
        """
        return self._zIndex

    def getRepresentation(self) -> Representation:
        """ This method is used to get the representation of an object
        @return  The representation of the object
        """
        return self._representation

    def getPose(self) -> Pose:
        """ This method is used to get the position and the orientation of an object
        @return  The position and the orientation of an object
        """
        return self._pose

    def getID(self) -> str:
        """ This method is used to get the ID of an object
        @return  The ID of the object
        """
        return self._id

    def getVisibilityLocked(self) -> bool:
        """ This method allows to know if the visibility of an object is locked
        @return  If the visibility of an object is locked
        """
        return self._visibilityLocked

    def getEnvironment(self) :
        """ This method is used to get the environment of an object
        @return The environment of the object
        """
        return self._environment

    def getCollidedState(self) -> bool:
        return self._isCollided

    def getIntersectionsWith(self,obj) -> List[QPointF]:
        return self.getRepresentation().getShape().getIntersectionsWith(obj.getRepresentation().getShape())

    def paint(self, painter:QPainter):
        self._representation.paint(painter)

    def isVisible(self) -> bool:
        """ This method is used to know if an object is visible or not
        @return  If the object is visible
        """
        return self._representation.isVisible()

    def toggleVisible(self):
        if not self._visibilityLocked:
            self._representation.toggleVisible()
            self.visibylityChanged()

    def visibylityChanged(self):
        if hasattr(self,'getComponents'):
            for comp in self.getComponents():
                comp.setVisibilityLocked(not self.isVisible())
            if not self.isVisible():
                if self.getOdometryDrawn():
                    self.hideOdometry()
                    self.toggleOdometryDrawn()
                if self.getTrajectoryDrawn():
                    self.hideTrajectory()
                    self.toggleTrajectoryDrawn()
        self.notifyObservers("visibilityChanged")

    def completeID(self):
        self._id+="_"+str(Object.__number_of_instances[self._id])

    def isSelected(self) -> bool:
        """ This method is used to know if an object is selected
        @return  If the object is selected
        """
        return self._isSelected

    def isCollided(self):
        if not self._isCollided:
            for obj in self._environment.getObjects():
                if self!=obj and self.isCollidedWith(obj):
                    self._isCollided=True
                    obj.setCollidedState(True)

    def isCollidedWith(self,obj) -> bool:
        return len(self.getIntersectionsWith(obj))!=0

    def accelerationChanged(self,sender):
        self._acceleration=sender.getAcceleration()