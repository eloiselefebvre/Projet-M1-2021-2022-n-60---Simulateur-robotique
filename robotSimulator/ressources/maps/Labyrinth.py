import random

from robotSimulator import Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line


class Labyrinth():

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 2
    INTERVAL_SIZE = 180


    def __init__(self,environment):
        self._environment = environment
        self._width = 1594
        self._height = 910
        self._nbColumn = self._width//self.INTERVAL_SIZE
        self._nbLine = self._height//self.INTERVAL_SIZE
        self.drawGrid()


    def drawGrid(self):
        for i in range(self._nbLine+1):
            for j in range(self._nbColumn+1):
                print("i:",i)
                print("j:", j)

                probability=random.randint(1, 2)
                if probability==1:
                    if j!=0 and j!= self._nbColumn:
                        if j!=0:
                            self._environment.addObject(Object(Representation(Line(self.INTERVAL_SIZE, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))),j*self.INTERVAL_SIZE,i*self.INTERVAL_SIZE)
                    if j==self._nbColumn:
                        self._environment.addObject(Object(Representation(Line(self.INTERVAL_SIZE+self._width-j*self.INTERVAL_SIZE, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))),j*self.INTERVAL_SIZE,i*self.INTERVAL_SIZE)
                if probability==2:
                    if i!=0 and i!= self._nbLine:
                        self._environment.addObject(Object(Representation(Line(self.INTERVAL_SIZE, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))),j*self.INTERVAL_SIZE,i*self.INTERVAL_SIZE,-90)
                    if i==self._nbLine:
                        self._environment.addObject(Object(Representation(Line(self.INTERVAL_SIZE+self._height-i*self.INTERVAL_SIZE, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))),j*self.INTERVAL_SIZE,i*self.INTERVAL_SIZE,-90)















