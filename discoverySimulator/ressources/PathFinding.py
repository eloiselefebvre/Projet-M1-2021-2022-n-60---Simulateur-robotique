import threading
import time
from math import sqrt, atan, degrees, cos, radians, sin, acos, ceil
from typing import Tuple

from PyQt5.QtCore import QPoint, QLineF

from discoverySimulator.Pose import Pose
from discoverySimulator.Object import Object
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Rectangle, Line
from discoverySimulator.robots import Robot


class PathFinding:

    """The PathFinding class provides a path finding for a robot."""

    # TODO : Pause sur pathfinding ?? sync sur sim ?

    __MOVES = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    __COLORS = {
        "closed_node": "#40C9E0",
        "opened_node":"#22A6B3",
        "computed_node" : "#FFFDC7",
        "path_node": "#FFFE60",
        "begin_node": "#45EB0E",
        "end_node": "#E8221E",
        "simplified_path":"#F9886A"
    }

    __CELL_SIZE = 15
    __CELL_OFFSET = __CELL_SIZE / 2

    def __init__(self, environment,securityMargin:float=0,displayEnabled:bool=False ,displayDelay:float=0.01):
        """
        Constructs a pathfinding.
        @param environment  Environment where the pathfinding will take place
        @param displayEnabled  The display of the pathfinding [bool]
        @param displayDelay  The delay of the display [s]
        """
        self._environment=environment
        self._displayEnabled = displayEnabled
        self._displayDelay = displayDelay

        self._obstaclesShapeWithOffset=[obj.getRepresentation().getShape().offset(securityMargin,True) for obj in self._environment.getObjects() if not isinstance(obj, Robot)]
        # for obs in self._obstaclesShapeWithOffset:
        #     self._environment.addVirtualObject(Object(Representation(obs)),obs.getPose().getX(),obs.getPose().getY(),obs.getPose().getOrientation())

        self.__ROWS_NUMBER = ceil(self._environment.getWidth() / PathFinding.__CELL_SIZE)
        self.__COLS_NUMBER = ceil(self._environment.getHeight() / PathFinding.__CELL_SIZE)
        self._nodes = {}
        self.__endNode=None
        self.__beginNode=None

        self._nextPointIndex = 0

    def findPath(self,begin,end,callback=None):
        if self.__setBeginNode((int(begin[0]/PathFinding.__CELL_SIZE), int(begin[1] / PathFinding.__CELL_SIZE))) and self.__setEndNode((int(end[0] / PathFinding.__CELL_SIZE), int(end[1] / PathFinding.__CELL_SIZE))):
            th = threading.Thread(target=self.__astar,args=[callback])
            th.start()
        else:
            if callback is not None:
                callback(None)

    def __setBeginNode(self, node):
        if self.__getNodeValue(node) and self.__isValidNode(node):
            self.__createNode(node)
            self.__beginNode = node
            if self._displayEnabled:
                self.__setNodeColor(self.__beginNode, self.__COLORS['begin_node'])
            return True
        return False

    def __setEndNode(self, node):
        if self.__getNodeValue(node) and self.__isValidNode(node):
            self.__createNode(node)
            self.__endNode = node
            if self._displayEnabled:
                self.__setNodeColor(self.__endNode, self.__COLORS['end_node'])
            return True
        return False

    def __setNodeColor(self, node, color):
        self._nodes[node].setColor(color)

    def __getNodeValue(self, node:Tuple[int,int]=(0,0)):
        for shape in self._obstaclesShapeWithOffset:
            if shape.contains(QPoint(node[0] * PathFinding.__CELL_SIZE, node[1] * PathFinding.__CELL_SIZE)) or \
                    shape.contains(
                        QPoint(node[0] * PathFinding.__CELL_SIZE, (node[1] + 1) * PathFinding.__CELL_SIZE)) or \
                    shape.contains(
                        QPoint((node[0] + 1) * PathFinding.__CELL_SIZE, node[1] * PathFinding.__CELL_SIZE)) or \
                    shape.contains(
                        QPoint((node[0] + 1) * PathFinding.__CELL_SIZE, (node[1] + 1) * PathFinding.__CELL_SIZE)):
                return False
        return True

    def __getNodeNeighbors(self, node):
        nodes = []
        for mv in self.__MOVES:
            i = node[0] + mv[0]
            j = node[1] + mv[1]
            n_node = (i, j)
            if self.__isValidNode(n_node) and self.__getNodeValue(n_node):
                nodes.append(n_node)
        return nodes

    def __isValidNode(self, node):
        return node[0] >= 0 and node[0] < self.__ROWS_NUMBER and node[1] >= 0 and node[1] < self.__COLS_NUMBER

    def __astar(self,callback=None):
        predecessors = {self.__beginNode: None}
        opened_nodes = {self.__beginNode: 0}
        closed_nodes = {}
        opened_nodes_heuristic = {self.__beginNode: self.__heuristic(self.__beginNode)}

        current = self.__beginNode
        while current != self.__endNode:
            closed_nodes[current] = opened_nodes.pop(current)
            opened_nodes_heuristic.pop(current)
            if current != self.__beginNode and current != self.__endNode and self._displayEnabled:
                self.__setNodeColor(current, self.__COLORS['closed_node'])
                time.sleep(self._displayDelay)
            neighbors = self.__getNodeNeighbors(current)
            for n in neighbors:
                if not n in closed_nodes:
                    distanceFromBeginNode = closed_nodes[current] + ((n[0]-current[0])**2+(n[1]-current[1])**2)**0.5
                    if n in opened_nodes:
                        if distanceFromBeginNode < opened_nodes[n]:
                            opened_nodes[n] = distanceFromBeginNode
                            opened_nodes_heuristic[n] = opened_nodes[n] + self.__heuristic(n)
                            predecessors[n] = current
                    else:
                        if n != self.__beginNode and n!= self.__endNode and self._displayEnabled:
                            self.__createNode(n)
                            self.__setNodeColor(n, self.__COLORS["opened_node"])

                        opened_nodes[n] = distanceFromBeginNode
                        opened_nodes_heuristic[n] = opened_nodes[n] + self.__heuristic(n)

                        predecessors[n] = current
            if len(opened_nodes_heuristic)==0:
                if callback is not None:
                    callback(None)
                return
            current = min(opened_nodes_heuristic,key=opened_nodes_heuristic.__getitem__)

            if current != self.__beginNode and current != self.__endNode and self._displayEnabled:
                self.__setNodeColor(current, self.__COLORS["computed_node"])

            time.sleep(0.01)

        path = []
        current = self.__endNode
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        if self._displayEnabled:
            for p in path:
                if p != self.__beginNode and p != self.__endNode:
                    self.__setNodeColor(p, self.__COLORS["path_node"])
        if callback is not None:
            callback(self.simplifyPath(path))

    def __heuristic(self, node):
        return self.__manhattanDistance(node,self.__endNode)

    def __manhattanDistance(self, node1,node2):
        return abs(node2[0] - node1[0]) + abs(node2[1] - node1[1])

    def __euclidDistance(self, node1,node2):
        return ((node2[0] - node1[0]) ** 2 + (node2[1] - node1[1]) ** 2) ** 0.5

    def __createNode(self, node):
        self._nodes[node]=Rectangle(15, 15)
        if self._displayEnabled:
            self._environment.addVirtualObject(Object(Representation(self._nodes[node])), node[0] * self.__CELL_SIZE + self.__CELL_OFFSET, node[1] * self.__CELL_SIZE + self.__CELL_OFFSET)
        else:
            self._nodes[node].setPose(Pose(node[0] * self.__CELL_SIZE + self.__CELL_OFFSET, node[1] * self.__CELL_SIZE + self.__CELL_OFFSET))


    def simplifyPath(self, path):
        counter=1
        lastPoint = path[0]
        current=0
        line=None
        points=[path[0]]

        for i in range(1,len(path)):

            nextPoint = path[current+counter]

            length = sqrt(((lastPoint[0] * self.__CELL_SIZE + self.__CELL_OFFSET) - (nextPoint[0] * self.__CELL_SIZE + self.__CELL_OFFSET)) ** 2 + ((lastPoint[1] * self.__CELL_SIZE + self.__CELL_OFFSET) - (nextPoint[1] * self.__CELL_SIZE + self.__CELL_OFFSET)) ** 2)
            dx = nextPoint[0] * self.__CELL_SIZE + self.__CELL_OFFSET - (lastPoint[0] * self.__CELL_SIZE + self.__CELL_OFFSET)
            dy = nextPoint[1] * self.__CELL_SIZE + self.__CELL_OFFSET - (lastPoint[1] * self.__CELL_SIZE + self.__CELL_OFFSET)

            if dy != 0:
                theta = degrees(atan(dx / dy))
                if dy<0:
                    orientation=180-degrees(atan(dx / dy))
                else :
                    if theta>0:
                        orientation=-theta
                    else :
                        orientation = 360-theta
            else :
                if dx>0:
                    orientation=270
                else :
                    orientation=90
            if self._displayEnabled and line is not None:
                self._environment.removeVirtualObject(line)
            line = Object(Representation(Line(int(length), 5, self.__COLORS["simplified_path"])))
            if self._displayEnabled:
                self._environment.addVirtualObject(line, lastPoint[0] * self.__CELL_SIZE + self.__CELL_OFFSET, lastPoint[1] * self.__CELL_SIZE + self.__CELL_OFFSET, orientation)
            else:
                line.setPose(Pose(lastPoint[0] * self.__CELL_SIZE + self.__CELL_OFFSET, lastPoint[1] * self.__CELL_SIZE + self.__CELL_OFFSET, orientation))

            for obj in self._obstaclesShapeWithOffset:
                if obj.getIntersectionsWith(line.getRepresentation().getShape()):
                    lastPoint=path[i]
                    line=None
                    current=i
                    counter=0
                    points.append((lastPoint[0],lastPoint[1]))
                    break
            counter+=1
        points.append((path[-1][0],path[-1][1]))
        return [(x * self.__CELL_SIZE + self.__CELL_OFFSET, y * self.__CELL_SIZE + self.__CELL_OFFSET) for x, y in points]

