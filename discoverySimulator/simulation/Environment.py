from PyQt5.QtCore import QSize
from discoverySimulator import Object, Pose
from discoverySimulator.Frame import Frame
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Line
from discoverySimulator.robots import Robot
from discoverySimulator.sensors import Sensor

from typing import List

class Environment:

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 2

    def __init__(self,width:int,height:int):
        """
        This method is used to create an environment
        :param width: width of the environment [px]
        :param height: height of the environment [px]
        """
        self.__objects=[]
        self.__virtualObjects=[]
        self.__sensors=[]

        self.__size = QSize(int(width),int(height))
        self.__frame=Frame(Pose(0, 0))

        self.__hasWalls=False
        self.__drawWalls()

    def getObjects(self) -> List[Object]:
        return self.__objects

    def getVirtualObjects(self) -> List[Object]:
        return self.__virtualObjects

    def getSensors(self) -> List[Sensor]:
        return self.__sensors

    def getFrame(self) -> Frame:
        return self.__frame

    def getSize(self) -> QSize:
        return self.__size

    def getWidth(self) -> int:
        return self.__size.width()

    def getHeight(self) -> int:
        return self.__size.height()

    def hasWalls(self) -> bool:
        return self.__hasWalls

    def addObject(self, object:Object, x:float=0, y:float=0, orientation:float=0):
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
            object.getFrame().setBaseFrame(self.__frame)
            object.getFrame().setCoordinates(pose)
            self.__objects.append(object)
            if isinstance(object, Robot):
                for comp in object.getComponents():
                    comp.setEnv(self)
                    if isinstance(comp, Sensor):
                        self.__addSensor(comp)
                object.setOdometryPose(pose.copy())
            if isinstance(object, Sensor):
                self.__addSensor(object)

    def addVirtualObject(self, virtualObject:Object, x:float=0, y:float=0, orientation:float=0):
        """
           This method allows to add a virtual object in the environment
           :param virtualObject: object of the class Object or which inherits from Object
           :param x: x coordinate of the object in the environment [px]
           :param y: y coordinate of the object in the environment [px]
           :param orientation: orientation of the object in the environment [degrees]
        """
        if isinstance(virtualObject, Object):
            virtualObject.setPose(Pose(x, y, orientation))
            virtualObject.setEnv(self)
            self.__virtualObjects.append(virtualObject)

    def removeObject(self, object:Object):
        if object in self.__objects:
            self.__objects.remove(object)

    def removeVirtualObject(self, virtualObject:Object):
        if virtualObject in self.__virtualObjects:
            self.__virtualObjects.remove(virtualObject)

    def __addSensor(self,sensor:Sensor):
        if isinstance(sensor,Sensor):
            self.__sensors.append(sensor)

    def __drawWalls(self):
        if not self.__hasWalls:
            self.addObject(Object(Representation(Line(self.__size.height(), Environment.DEFAULT_BORDER_SCREEN_WIDTH, Environment.DEFAULT_BORDER_SCREEN_COLOR))), 0, 0)
            self.addObject(Object(Representation(Line(self.__size.height(), Environment.DEFAULT_BORDER_SCREEN_WIDTH, Environment.DEFAULT_BORDER_SCREEN_COLOR))), self.__size.width(), 0)
            self.addObject(Object(Representation(Line(self.__size.width(), Environment.DEFAULT_BORDER_SCREEN_WIDTH, Environment.DEFAULT_BORDER_SCREEN_COLOR))), 0, 0, -90)
            self.addObject(Object(Representation(Line(self.__size.width(), Environment.DEFAULT_BORDER_SCREEN_WIDTH, Environment.DEFAULT_BORDER_SCREEN_COLOR))), 0, self.__size.height(), -90)
            self.__hasWalls=True