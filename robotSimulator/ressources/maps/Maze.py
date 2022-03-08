import random

from robotSimulator import Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line


class Maze:

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 2
    INTERVAL_SIZE = 150


    def __init__(self,environment):
        self._environment = environment
        self._width = self._environment.getSize().width()
        self._height = self._environment.getSize().height()
        self._nbColumn = self._width//self.INTERVAL_SIZE
        self._nbLine = self._height//self.INTERVAL_SIZE
        self._mazeElements = []

    def drawGrid(self):
        for i in range(self._nbLine+1):
            for j in range(self._nbColumn+1):
                if random.randint(0,1):
                    if j!=0:
                        dh=self._height%self.INTERVAL_SIZE if i==self._nbLine else self.INTERVAL_SIZE
                        self._mazeElements.append(Object(Representation(Line(dh, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))))
                        self._environment.addObject(self._mazeElements[-1],j*self.INTERVAL_SIZE,i*self.INTERVAL_SIZE)
                else:
                    if i!=0:
                        dw=self._width%self.INTERVAL_SIZE if j==self._nbColumn else self.INTERVAL_SIZE
                        self._mazeElements.append(Object(Representation(Line(dw, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))))
                        self._environment.addObject(self._mazeElements[-1],j*self.INTERVAL_SIZE,i*self.INTERVAL_SIZE,-90)


    def deleteGrid(self):
        for item in self._mazeElements:
            self._environment.removeObject(item)
        self._mazeElements=[]

    def getWalls(self):
        return self._mazeElements

