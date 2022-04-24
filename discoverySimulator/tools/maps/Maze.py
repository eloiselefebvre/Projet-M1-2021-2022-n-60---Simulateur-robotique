import random
from typing import List

from discoverySimulator import Object
from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Line


class Maze:

    """ The Maze class provides a maze."""

    __DEFAULT_BORDER_SCREEN_WIDTH = 2
    __INTERVAL_SIZE = 300

    def __init__(self,environment):
        """ Constructs a maze in the given environment.
        @param environment  Environment where the maze will be added
        """
        self._environment = environment
        self._width = self._environment.getSize().width()
        self._height = self._environment.getSize().height()
        self._nbColumn = self._width//Maze.__INTERVAL_SIZE
        self._nbLine = self._height//Maze.__INTERVAL_SIZE
        self._mazeElements = []

    def draw(self):
        """ Draws the maze."""
        for i in range(self._nbLine+1):
            for j in range(self._nbColumn+1):
                if random.randint(0,1):
                    if j!=0:
                        dh=self._height%Maze.__INTERVAL_SIZE if i == self._nbLine else Maze.__INTERVAL_SIZE
                        self._mazeElements.append(Object(Representation(Line(dh, Maze.__DEFAULT_BORDER_SCREEN_WIDTH,colors['tundora']))))
                        self._environment.addObject(self._mazeElements[-1], j * Maze.__INTERVAL_SIZE, i * Maze.__INTERVAL_SIZE)
                else:
                    if i!=0:
                        dw=self._width%Maze.__INTERVAL_SIZE if j == self._nbColumn else Maze.__INTERVAL_SIZE
                        self._mazeElements.append(Object(Representation(Line(dw, Maze.__DEFAULT_BORDER_SCREEN_WIDTH,colors['tundora']))))
                        self._environment.addObject(self._mazeElements[-1], j * Maze.__INTERVAL_SIZE, i * Maze.__INTERVAL_SIZE, -90)

    def delete(self):
        """ Deletes the maze."""
        for item in self._mazeElements:
            self._environment.removeObject(item)
        self._mazeElements.clear()



