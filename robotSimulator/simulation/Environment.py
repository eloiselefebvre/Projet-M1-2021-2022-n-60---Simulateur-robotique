from robotSimulator import Object, Pose
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line

class Environment:

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 2

    def __init__(self):
        self._objects=[]
        self._virtualObjects=[]
        self._hasWalls=False


    def addObject(self,obj,x=0,y=0,orientation=0):
        if isinstance(obj, Object):
            obj.setPose(Pose(x,y,orientation))
            obj.setEnv(self)
            self._objects.append(obj)


    def addVirtualObject(self,obj,x=0,y=0,orientation=0):
        if isinstance(obj, Object):
            obj.setPose(Pose(x,y,orientation))
            obj.setEnv(self)
            self._virtualObjects.append(obj)

    def removeObject(self,obj):
        if obj in self._objects:
            self._objects.remove(obj)


    def removeVirtualObject(self,obj):
        if obj in self._virtualObjects:
            self._virtualObjects.remove(obj)

    def putObjectInForeground(self,obj):
        if obj in self._objects:
            self._objects.remove(obj)
            self._objects.append(obj)

    def getObjects(self):
        return self._objects

    def getVirtualObjects(self):
        return self._virtualObjects

    def hasWalls(self):
        return self._hasWalls

    def drawWalls(self,w,h):
        if not self._hasWalls:
            self.addObject(Object(Representation(Line(h,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,0)
            self.addObject(Object(Representation(Line(h,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),w,0)
            self.addObject(Object(Representation(Line(w,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,0,-90)
            self.addObject(Object(Representation(Line(w,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,h,-90)
            self._hasWalls=True

