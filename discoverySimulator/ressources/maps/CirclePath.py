import random
from typing import List

from discoverySimulator import Object
from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle


class CirclePath:

    DEFAULT_WIDTH=20

    def  __init__(self, environment, color=colors['widgetBorder']):
        """ This method is used to create a circle path
        @param environment  The environment where the circle path will take place
        @param color  Color of the circle path
        """
        self._environment = environment
        self._color = color
        self._pathElements = []
        self.drawPath()

    # GETTERS
    def getElements(self) -> List[Circle]:
        """ This method allows to get all the elements of the path
        @return  All the elements
        """
        return self._pathElements

    def drawPath(self):
        numberOfCircle=random.randint(1,2)
        if numberOfCircle==1:
            radius=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/2))
            circle1 = Object(Representation(Circle(radius,self._color)))
            circle2 = Object(Representation(Circle(radius-20,colors['sceneBackground'])))
            self._environment.addVirtualObject(circle1,int(self._environment.getWidth()/2),int(self._environment.getHeight()/2))
            self._environment.addVirtualObject(circle2, int(self._environment.getWidth() / 2),int(self._environment.getHeight() / 2))
            self._pathElements.append(circle1)
            self._pathElements.append(circle2)

        else:
            radius1=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/4))
            radius2=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/4))
            circle1 = Object(Representation(Circle(radius1, self._color)))
            circle2 = Object(Representation(Circle(radius1 - 20, colors['sceneBackground'])))
            circle3 = Object(Representation(Circle(radius2,self._color)))
            circle4 = Object(Representation(Circle(radius2-20,colors['sceneBackground'])))
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





