import time

from robotSimulator import Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Rectangle


class PathFinding:

    MOVES = [(-1, 0), (0, 1), (1, 0), (0,-1)]
    DISPLAY_DELAY = 0
    COLORS = {
        "closed_node": "#40C9E0",
        "opened_node":"#22A6B3",
        "computed_node" : "#FFFDC7",
        "path_node": "#FFFE60",
        "begin_node": "#30336B",
        "end_node": "#30336B"
    }

    def __init__(self, environment, NODE=None):
        self._environment=environment

        self.__ROWS_NUMBER = (self._environment.getWidth())/15
        self.__COLS_NUMBER = (self._environment.getHeight())/15

        self.__beginNode = (10,10)
        self.__endNode = (20,20)
        self._nodes = {}
        self.createNode(self.__beginNode)
        self.__astar()

    def __setBeginNode(self, node):
        if self.__getNodeValue(node) and self.__isValidNode(node):
            self.__beginNode = node
            return True
        return False

    def __setEndNode(self, node):
        if self.__getNodeValue(node) and self.__isValidNode(node):
            self.__endNode = node
            return True
        return False

    def __setNodeColor(self, node, color):
        self._nodes[node].setColor(color)
        self.__refreshDisplay()

    def __getNodeValue(self, node):
        return True

    def __getNodeNeighbors(self, node):
        nodes = []
        for mv in self.MOVES:
            i = node[0] + mv[0]
            j = node[1] + mv[1]
            n_node = (i, j)
            if self.__isValidNode(n_node) and self.__getNodeValue(n_node):
                nodes.append(n_node)
        return nodes

    def __isValidNode(self, node):
        return node[0] >= 0 and node[0] < self.__ROWS_NUMBER and node[1] >= 0 and node[1] < self.__COLS_NUMBER

    def __refreshDisplay(self):
        pass

    def __drawBeginNode(self):
        pass

    def __drawEndNode(self, background):
        pass

    def findShortestPathWith(self, algorithm):
       pass

    def __astar(self):
        predecessors = {self.__beginNode: None}
        opened_nodes = {self.__beginNode: 0}
        closed_nodes = {}
        opened_nodes_heuristic = {self.__beginNode: self.__heuristic(self.__beginNode)}

        current = self.__beginNode
        while current != self.__endNode:
            time.sleep(.01)
            closed_nodes[current] = opened_nodes.pop(current)
            opened_nodes_heuristic.pop(current)
            self.__setNodeColor(current, self.COLORS['closed_node'])
            neighbors = self.__getNodeNeighbors(current)
            for n in neighbors:
                if not n in closed_nodes:
                    distanceFromBeginNode = closed_nodes[current] + 1
                    if n in opened_nodes:
                        if distanceFromBeginNode < opened_nodes[n]:
                            opened_nodes[n] = distanceFromBeginNode
                            opened_nodes_heuristic[n] = opened_nodes[n] + self.__heuristic(n)
                            predecessors[n] = current
                    else:
                        self.createNode(n)
                        opened_nodes[n] = distanceFromBeginNode
                        opened_nodes_heuristic[n] = opened_nodes[n] + self.__heuristic(n)
                        self.__setNodeColor(n, self.COLORS["opened_node"])
                        predecessors[n] = current
            current = min(opened_nodes_heuristic,key=opened_nodes_heuristic.__getitem__)
            self.__setNodeColor(current, self.COLORS["computed_node"])
        self.__displayFoundPathAndDistance(predecessors,opened_nodes)

    def __displayFoundPathAndDistance(self, predecessors, opened_nodes):
        path = []
        current = self.__endNode
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        for p in path:
            self.__setNodeColor(p, self.COLORS["path_node"])

    def __heuristic(self, node):
        return self.__euclidDistanceToEnd(node)

    def __manhattanDistanceToEnd(self, node):
        return abs(self.__endNode[0] - node[0]) + abs(self.__endNode[1] - node[1])

    def __euclidDistanceToEnd(self, node):
        return ((self.__endNode[0] - node[0]) ** 2 + (self.__endNode[1] - node[1]) ** 2) ** 0.5

    def createNode(self,node):
        self._nodes[node]=Rectangle(15, 15, "#FF9900")
        self._environment.addVirtualObject(Object(Representation(self._nodes[node])),node[0]*15+15/2,node[1]*15+15/2)

