from PyQt5.QtCore import QSize
from discoverySimulator import Object, Pose
from discoverySimulator.Frame import Frame
from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Line
from discoverySimulator.robots import Robot
from discoverySimulator.sensors import Sensor

from typing import List

class Environment:

    DEFAULT_BORDER_SCREEN_WIDTH = 2

    DEFAULT_NOISE_STRENGH = 0.05

    # Available models : virtual (perfect), real (with noise)
    def __init__(self,width:int,height:int,model:str='virtual'):
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

        self.__model=model

        self.__hasWalls=False
        self.__drawWalls()

        self._noiseStrengh = Environment.DEFAULT_NOISE_STRENGH

    # GETTERS
    def getObjects(self) -> List[Object]:
        """
        This method is used to get all the objects of the environment
        :return: all the objects of the environment
        """
        return self.__objects

    def getVirtualObjects(self) -> List[Object]:
        """
        This method is used to get all the virtuals objects of the environment
        :return: all the virtuals objects of the environment
        """
        return self.__virtualObjects

    def getSensors(self) -> List[Sensor]:
        """
        This method is used to get all the sensors of the environment
        :return: all the sensors of the environment
        """
        return self.__sensors

    def getFrame(self) -> Frame:
        return self.__frame

    def getSize(self) -> QSize:
        return self.__size

    def getWidth(self) -> int:
        """
        This method is used to get the width of the environment
        :return: the width of the environment [px]
        """
        return self.__size.width()

    def getHeight(self) -> int:
        """
        This method is used to get the height of the environment
        :return: the height of the environment [px]
        """
        return self.__size.height()

    def hasWalls(self) -> bool:
        return self.__hasWalls

    def isReal(self):
        return self.__model=="real"

    def setNoiseStrengh(self,noise):
        self._noiseStrengh=noise

    def getNoiseStrengh(self):
        return self._noiseStrengh

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
            object.setEnvironnement(self)
            object.getFrame().setBaseFrame(self.__frame)
            object.getFrame().setCoordinates(pose)
            self.__objects.append(object)
            if isinstance(object, Robot):
                for comp in object.getComponents():
                    comp.setEnvironnement(self)
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
            virtualObject.setEnvironnement(self)
            self.__virtualObjects.append(virtualObject)

    def removeObject(self, object:Object):
        """
        This method is used to remove an object of the environment
        :param object: object to remove
        """
        if object in self.__objects:
            self.__objects.remove(object)

    def removeVirtualObject(self, virtualObject:Object):
        """
        This method is used to remove a virtual object of the environment
        :param object: object to remove
        """
        if virtualObject in self.__virtualObjects:
            self.__virtualObjects.remove(virtualObject)

    def __addSensor(self,sensor:Sensor):
        if isinstance(sensor,Sensor):
            self.__sensors.append(sensor)

    def __drawWalls(self):
        if not self.__hasWalls:
            self.addObject(Object(Representation(Line(self.__size.height(), Environment.DEFAULT_BORDER_SCREEN_WIDTH, colors['borderScreen']))), 0, 0)
            self.addObject(Object(Representation(Line(self.__size.height(), Environment.DEFAULT_BORDER_SCREEN_WIDTH, colors['borderScreen']))), self.__size.width(), 0)
            self.addObject(Object(Representation(Line(self.__size.width(), Environment.DEFAULT_BORDER_SCREEN_WIDTH, colors['borderScreen']))), 0, 0, -90)
            self.addObject(Object(Representation(Line(self.__size.width(), Environment.DEFAULT_BORDER_SCREEN_WIDTH, colors['borderScreen']))), 0, self.__size.height(), -90)
            self.__hasWalls=True