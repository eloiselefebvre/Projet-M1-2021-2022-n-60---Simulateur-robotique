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
        self.drawGrid()

    def drawGrid(self):
        for i in range(self._nbLine+1):
            for j in range(self._nbColumn+1):

                if random.randint(0,1):
                    if j!=0:
                        dh=self._height%self.INTERVAL_SIZE if i==self._nbLine else self.INTERVAL_SIZE
                        self._environment.addObject(Object(Representation(Line(dh, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))),j*self.INTERVAL_SIZE,i*self.INTERVAL_SIZE)
                else:
                    if i!=0:
                        dw=self._width%self.INTERVAL_SIZE if j==self._nbColumn else self.INTERVAL_SIZE
                        self._environment.addObject(Object(Representation(Line(dw, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))),j*self.INTERVAL_SIZE,i*self.INTERVAL_SIZE,-90)















