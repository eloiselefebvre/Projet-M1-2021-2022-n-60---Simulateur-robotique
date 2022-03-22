from PyQt5.QtCore import QSize
from discoverySimulator import Object, Pose
from discoverySimulator.Frame import Frame
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Line
from discoverySimulator.robots import Robot
from discoverySimulator.sensors import Sensor


class Environment:

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 2

    def __init__(self,width,height):
        """
        This method is used to create an environment
        :param width: width of the environment [px]
        :param height: height of the environment [px]
        """
        self._objects=[]
        self._virtualObjects=[]
        self._hasWalls=False
        self._size = QSize(width,height)

        self._frame=Frame(Pose(0,0))

        self._sensors=[]
        self.drawWalls()


    def getFrame(self):
        return self._frame

    def addObject(self, object, x=0, y=0, orientation=0):
        """
        This method allows to add an object in the environment
        :param object: object of the class Object or which inherits from Object
        :param x: x coordinate of the object in the environment [px]
        :param y: y coordinate of the object in the environment [px]
        :param orientation: orientation of the object in the environment [degrees]
        """
        if isinstance(object, Object):
            pose=Pose(x,y,orientation)
            object.setPose(pose)
            object.setEnv(self)
            object.getFrame().setBaseFrame(self._frame)
            object.getFrame().setCoordinates(pose)
            self._objects.append(object)
            if isinstance(object, Robot):
                for comp in object.getComponents():
                    comp.setEnv(self)
                    if isinstance(comp, Sensor):
                        self.__addSensor(comp)
                object.setOdometryPose(pose.copy())
            if isinstance(object, Sensor):
                self.__addSensor(object)

    def __addSensor(self,sensor):
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

    def setSize(self,size): # QSize
        self._size=size

    def getSize(self):
        return self._size

    def getWidth(self):
        return self._size.width()

    def getHeight(self):
        return self._size.height()