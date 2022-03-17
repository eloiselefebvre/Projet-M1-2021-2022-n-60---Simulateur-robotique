import random
from math import sqrt, atan, degrees

from discoverySimulator import Object
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Point, Rectangle, Circle


class CirclePath:

    DEFAULT_WIDTH=20
    DEFAULT_PATH_COLOR="#444444"

    def  __init__(self, environment, color="#444444"):
        self._environment = environment
        self._color = color
        self._pathElements = []
        self.drawPath()

    def drawPath(self):

        numberOfCircle=random.randint(1,2)

        if numberOfCircle==1:
            radius=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/2))
            circle1 = Object(Representation(Circle(radius,self._color)))
            circle2 = Object(Representation(Circle(radius-20,"#f0f0f0")))
            self._environment.addVirtualObject(circle1,int(self._environment.getWidth()/2),int(self._environment.getHeight()/2))
            self._environment.addVirtualObject(circle2, int(self._environment.getWidth() / 2),int(self._environment.getHeight() / 2))
            self._pathElements.append(circle1)
            self._pathElements.append(circle2)

        else:
            radius1=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/4))
            radius2=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/4))
            circle1 = Object(Representation(Circle(radius1, self._color)))
            circle2 = Object(Representation(Circle(radius1 - 20, "#f0f0f0")))
            circle3 = Object(Representation(Circle(radius2,self._color)))
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
        self._pathElements.clear()

    def getElements(self):
        return self._pathElements



