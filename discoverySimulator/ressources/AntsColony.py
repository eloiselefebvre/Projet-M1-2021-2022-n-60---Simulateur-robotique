from typing import Tuple

from discoverySimulator import Object
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Rectangle


class AntsColony():

    INTERVAL_SIZE = 15
    MOVES = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def __init__(self,environment):
        self._environment=environment
        envWidth=self._environment.getWidth()
        envHeight=self._environment.getHeight()
        self.__ROWS_NUMBER = int((envWidth)/self.INTERVAL_SIZE)
        self.__COLS_NUMBER = int((envHeight)/self.INTERVAL_SIZE)
        self._grid={}
        for i in range(1,self.__COLS_NUMBER+1):
            for j in range(1,self.__ROWS_NUMBER+1):
                self._grid[(i,j)]=0
        self.__endNode = (50,50)
        self._nodes=[]

    def gridValues(self,robot):
        currentPosition=(robot.getPose().getX(),robot.getPose().getY())
        if currentPosition!=self.__endNode:
            currentState=(int(currentPosition[0]/15),int(currentPosition[1]/15))
            self._grid[(currentState[0],currentState[1])]+=1
            self.__getNodeNeighbors(currentState)
            maxState = currentState
            for node in self._nodes:
                if self._grid[node]>self._grid[maxState]:
                    maxState=node

    def __getNodeNeighbors(self, node):
        nodes = []
        for mv in self.MOVES:
            i = node[0] + mv[0]
            j = node[1] + mv[1]
            n_node = (i, j)
            if self.__isValidNode(n_node):
                nodes.append(n_node)
                self._nodes.append(n_node)
        return nodes

    def __isValidNode(self, node):
        return node[0] >= 0 and node[0] < self.__ROWS_NUMBER and node[1] >= 0 and node[1] < self.__COLS_NUMBER









