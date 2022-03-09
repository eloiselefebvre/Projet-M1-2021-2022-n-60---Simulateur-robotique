from PyQt5.QtCore import QSize
from robotSimulator import Object, Pose
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line
from robotSimulator.robots import Robot
from robotSimulator.sensors import Sensor


class Environment:

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 2

    def __init__(self,width,height):
        self._width=width
        self._height=height
        self._objects=[]
        self._virtualObjects=[]
        self._hasWalls=False
        self._size = QSize(width,height)

        self._sensors=[]
        self._maze=False
        self._path=False
        self.drawWalls()

    def removeMaze(self):
        pass

    def addObject(self,obj,x=0,y=0,orientation=0):
        if isinstance(obj, Object):
            pose=Pose(x,y,orientation)
            obj.setPose(pose)
            obj.setEnv(self)
            self._objects.append(obj)
            if isinstance(obj,Robot):
                for comp in obj.getComponents():
                    if isinstance(comp, Sensor):
                        self.addSensor(comp)
                obj.setOdometryPose(pose.copy())
            if isinstance(obj,Sensor):
                self.addSensor(obj)

    def addSensor(self,sensor):
        self._sensors.append(sensor)

    def getSensors(self):
        return self._sensors

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

    def drawWalls(self):
        if not self._hasWalls:
            self.addObject(Object(Representation(Line(self._size.height(),self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,0)
            self.addObject(Object(Representation(Line(self._size.height(),self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),self._size.width(),0)
            self.addObject(Object(Representation(Line(self._size.width(),self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,0,-90)
            self.addObject(Object(Representation(Line(self._size.width(),self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,self._size.height(),-90)
            self._hasWalls=True

    def hasSize(self):
        return not self._size.isEmpty()

    def setSize(self,size): # QSize
        self._size=size

    def getSize(self):
        return self._size

    def hasMaze(self):
        return self._maze

    def setMaze(self,bool):
        self._maze = bool

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def setPath(self,bool):
        self._path=bool

    def hasPath(self):
        return self._path
