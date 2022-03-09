import random
from math import sqrt, atan, degrees

from robotSimulator import Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Point, Rectangle, Circle


class Path:

    DEFAULT_WIDTH=20
    DEFAULT_PATH_COLOR="#444444"

    def  __init__(self, environment):
        self._environment = environment
        self._pathElements = []

    def drawPath(self):

        numberOfCircle=random.randint(1,2)

        if numberOfCircle==1:
            radius=random.randint(200,int(self._environment.getWidth()/2))
            circle1 = Object(Representation(Circle(radius,"#444444")))
            circle2 = Object(Representation(Circle(radius-20,"#f0f0f0")))
            self._environment.addVirtualObject(circle1,int(self._environment.getWidth()/2),int(self._environment.getHeight()/2))
            self._environment.addVirtualObject(circle2, int(self._environment.getWidth() / 2),int(self._environment.getHeight() / 2))
            self._pathElements.append(circle1)
            self._pathElements.append(circle2)

        else:
            radius1=random.randint(200,int(self._environment.getWidth()/4))
            radius2=random.randint(200,int(self._environment.getWidth()/4))
            circle1 = Object(Representation(Circle(radius1, "#444444")))
            circle2 = Object(Representation(Circle(radius1 - 20, "#f0f0f0")))
            circle3 = Object(Representation(Circle(radius2,"#444444")))
            circle4 = Object(Representation(Circle(radius2-20,"#f0f0f0")))
            self._environment.addVirtualObject(circle1, int(self._environment.getWidth()/2)-radius1,int(self._environment.getHeight() / 2))
            self._environment.addVirtualObject(circle2, int(self._environment.getWidth()/2)-radius1,int(self._environment.getHeight() / 2))
            self._environment.addVirtualObject(circle3, int(self._environment.getWidth()/2)-20+radius2,int(self._environment.getHeight() / 2))
            self._environment.addVirtualObject(circle4, int(self._environment.getWidth()/2)-20+radius2,int(self._environment.getHeight() / 2))
            self._pathElements.append(circle1)
            self._pathElements.append(circle2)
            self._pathElements.append(circle2)
            self._pathElements.append(circle3)

    def deleteElements(self):
        for item in self._pathElements:
            self._environment.removeVirtualObject(item)
        self._pathElements = []

    def getElements(self):
        return self._pathElements



