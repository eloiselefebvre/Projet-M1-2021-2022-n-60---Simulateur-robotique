import time
from math import sqrt, atan, degrees, cos, radians, sin, acos
from PyQt5.QtCore import QPoint, QLineF

from discoverySimulator.Pose import Pose
from discoverySimulator.Object import Object
from discoverySimulator.Obstacle import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Rectangle, Circle, Point, Line


class PathFinding:

    MOVES = [(-1, 0),(-1,1), (0, 1),(1,1), (1, 0),(1,-1), (0,-1),(-1,-1)]
    DISPLAY_DELAY = 0
    COLORS = {
        "closed_node": "#40C9E0",
        "opened_node":"#22A6B3",
        "computed_node" : "#FFFDC7",
        "path_node": "#FFFE60",
        "begin_node": "#45EB0E",
        "end_node": "#E8221E",
        "simplified_path":"#F9886A"
    }
    FORWARD_SPEED = 200
    TURN_SPEED = 100
    CELL_SIZE = 15
    OFFSET = CELL_SIZE/2

    SECURITY_MARGIN = 20

    def __init__(self, environment, robot, displayEnabled=False ,displayDelay=0.01):
        self._environment=environment
        self._robot=robot
        self._robot.setIsFollowingPath(False)
        self._robot.setPathFinding(self)
        self._displayEnabled = displayEnabled
        self._displayDelay = displayDelay

        self._robot.setLeftWheelSpeed(0)
        self._robot.setRightWheelSpeed(0)
        self.__ROWS_NUMBER = (self._environment.getWidth())/15
        self.__COLS_NUMBER = (self._environment.getHeight())/15
        self._nodes = {}
        self.__endNode=None
        self.__setBeginNode((int(self._robot.getPose().getX()/self.CELL_SIZE),int(self._robot.getPose().getY()/self.CELL_SIZE)))

        self._pathSimplified=[]
        self._modifyOrientation = True
        self._nextPointIndex = 0

    def setEndPoint(self,mousePose):
        self.__endNode=(int(mousePose.x()/self.CELL_SIZE),int(mousePose.y()/self.CELL_SIZE))
        self.__setEndNode(self.__endNode)
        self.__astar()

    def setIsFollowingPath(self,state):
        self._robot.setIsFollowingPath(state)

    def __setBeginNode(self, node):
        if self.__getNodeValue(node) and self.__isValidNode(node):
            self.createNode(node)
            self.__beginNode = node
            if self._displayEnabled:
                self.__setNodeColor(self.__beginNode, self.COLORS['begin_node'])

    def __setEndNode(self, node):
        if self.__getNodeValue(node) and self.__isValidNode(node):
            self.createNode(node)
            self.__endNode = node
            if self._displayEnabled:
                self.__setNodeColor(self.__endNode, self.COLORS['end_node'])

    def __setNodeColor(self, node, color):
        self._nodes[node].setColor(color)

    def __getNodeValue(self, node):
        for obj in self._environment.getObjects():
            obstacle = obj.getRepresentation().getShape().offset(self._robot.getRepresentation().getShape().getBoundingBox().getWidth()/2+PathFinding.SECURITY_MARGIN) # TODO : Tableau d'obstacles offset pour ne pas tout recalculer tout le temps
            if isinstance(obj,Obstacle):
                if obstacle.contains(QPoint(node[0]*self.CELL_SIZE,node[1]*self.CELL_SIZE)) or\
                   obstacle.contains(QPoint(node[0]*self.CELL_SIZE,(node[1]+1)*self.CELL_SIZE)) or\
                   obstacle.contains(QPoint((node[0]+1)*self.CELL_SIZE,node[1]*self.CELL_SIZE)) or\
                   obstacle.contains(QPoint((node[0]+1)*self.CELL_SIZE,(node[1]+1)*self.CELL_SIZE)):
                    return False
        return True

    def __getNodeNeighbors(self, node):
        nodes = []
        for mv in self.MOVES:
            i = node[0] + mv[0]
            j = node[1] + mv[1]
            n_node = (i, j)
            if self.__isValidNode(n_node):
                nodes.append(n_node)
        return nodes

    def __isValidNode(self, node):
        return node[0] >= 0 and node[0] < self.__ROWS_NUMBER and node[1] >= 0 and node[1] < self.__COLS_NUMBER

    def __astar(self):
        predecessors = {self.__beginNode: None}
        opened_nodes = {self.__beginNode: 0}
        closed_nodes = {}
        opened_nodes_heuristic = {self.__beginNode: self.__heuristic(self.__beginNode)}

        current = self.__beginNode
        while current != self.__endNode:
            closed_nodes[current] = opened_nodes.pop(current)
            opened_nodes_heuristic.pop(current)
            if current != self.__beginNode and current != self.__endNode and self._displayEnabled:
                self.__setNodeColor(current, self.COLORS['closed_node'])
                time.sleep(self._displayDelay)
            neighbors = self.__getNodeNeighbors(current)
            for n in neighbors:
                weight = 0
                for ne in self.__getNodeNeighbors(n):
                    if not self.__getNodeValue(ne):
                        weight = 1
                        break
                if not n in closed_nodes and self.__getNodeValue(n):
                    distanceFromBeginNode = closed_nodes[current] + weight + ((n[0]-current[0])**2+(n[1]-current[1])**2)**0.5
                    if n in opened_nodes:
                        if distanceFromBeginNode < opened_nodes[n]:
                            opened_nodes[n] = distanceFromBeginNode
                            opened_nodes_heuristic[n] = opened_nodes[n] + self.__heuristic(n)
                            predecessors[n] = current
                    else:
                        if n != self.__beginNode and n!= self.__endNode and self._displayEnabled:
                            self.createNode(n)
                            self.__setNodeColor(n, self.COLORS["opened_node"])

                        opened_nodes[n] = distanceFromBeginNode
                        opened_nodes_heuristic[n] = opened_nodes[n] + self.__heuristic(n)

                        predecessors[n] = current
            current = min(opened_nodes_heuristic,key=opened_nodes_heuristic.__getitem__)

            if current != self.__beginNode and current != self.__endNode and self._displayEnabled:
                self.__setNodeColor(current, self.COLORS["computed_node"])

        self.__displayFoundPathAndDistance(predecessors)

    def __displayFoundPathAndDistance(self, predecessors):
        path = []
        current = self.__endNode
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        if self._displayEnabled:
            for p in path:
                if p != self.__beginNode and p != self.__endNode:
                    self.__setNodeColor(p, self.COLORS["path_node"])
        self._pathSimplified=self.simplifyPath(path)

    def __heuristic(self, node):
        return self.__euclidDistanceToEnd(node)

    def __manhattanDistanceToEnd(self, node):
        return abs(self.__endNode[0] - node[0]) + abs(self.__endNode[1] - node[1])

    def __euclidDistanceToEnd(self, node):
        return ((self.__endNode[0] - node[0]) ** 2 + (self.__endNode[1] - node[1]) ** 2) ** 0.5

    def createNode(self,node):
        self._nodes[node]=Rectangle(15, 15)
        if self._displayEnabled:
            self._environment.addVirtualObject(Object(Representation(self._nodes[node])),node[0]*self.CELL_SIZE+self.OFFSET,node[1]*self.CELL_SIZE+self.OFFSET)
        else:
            self._nodes[node].setPose(Pose(node[0]*self.CELL_SIZE+self.OFFSET,node[1]*self.CELL_SIZE+self.OFFSET))

    def followSimplifyPath(self):
        if self._robot.isFollowingPath():
            distance = sqrt((self._pathSimplified[self._nextPointIndex][0]-self._robot.getPose().getX())**2+(self._pathSimplified[self._nextPointIndex][1]-self._robot.getPose().getY())**2)
            angularDistance = self.angularDistance(self._pathSimplified[self._nextPointIndex])
            if (angularDistance>1 or angularDistance<-1) and self._modifyOrientation: # TODO : Attention aux déviations sur les longues distances ! -> Algo de suivi de ligne ?
                if angularDistance < 0:
                    self._robot.setRightWheelSpeed(-self.TURN_SPEED)
                    self._robot.setLeftWheelSpeed(self.TURN_SPEED)
                else:
                    self._robot.setRightWheelSpeed(self.TURN_SPEED)
                    self._robot.setLeftWheelSpeed(-self.TURN_SPEED)
            else:
                self._modifyOrientation=False
            if distance > 10 and not self._modifyOrientation:
                self._robot.setRightWheelSpeed(self.FORWARD_SPEED)
                self._robot.setLeftWheelSpeed(self.FORWARD_SPEED)
            else:
                if not self._modifyOrientation:
                    self._nextPointIndex+=1
                self._modifyOrientation=True
            if self._nextPointIndex==len(self._pathSimplified):
                self._robot.setRightWheelSpeed(0)
                self._robot.setLeftWheelSpeed(0)
                self._robot.setIsFollowingPath(False)

    def simplifyPath(self, path):
        counter=1
        lastPoint = path[0]
        current=0
        line=None
        points=[]

        for i in range(1,len(path)):

            nextPoint = path[current+counter]

            length = sqrt(((lastPoint[0]*self.CELL_SIZE+self.OFFSET)-(nextPoint[0]*self.CELL_SIZE+self.OFFSET))**2+((lastPoint[1]*self.CELL_SIZE+self.OFFSET)-(nextPoint[1]*self.CELL_SIZE+self.OFFSET))**2)
            dx = nextPoint[0]*self.CELL_SIZE+self.OFFSET-(lastPoint[0]*self.CELL_SIZE+self.OFFSET)
            dy = nextPoint[1]*self.CELL_SIZE+self.OFFSET-(lastPoint[1]*self.CELL_SIZE+self.OFFSET)

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
            line = Object(Representation(Line(int(length),5,self.COLORS["simplified_path"])))
            if self._displayEnabled:
                self._environment.addVirtualObject(line, int(lastPoint[0] * self.CELL_SIZE + self.OFFSET),int(lastPoint[1] * self.CELL_SIZE + self.OFFSET), orientation)
            else:
                line.setPose(Pose(int(lastPoint[0]*self.CELL_SIZE+self.OFFSET),int(lastPoint[1]*self.CELL_SIZE+self.OFFSET),orientation))

            for obj in self._environment.getObjects():
                if isinstance(obj,Obstacle):
                    if obj.getRepresentation().getShape().offset(self._robot.getRepresentation().getShape().getBoundingBox().getWidth()/2+PathFinding.SECURITY_MARGIN).getIntersectionsWith(line.getRepresentation().getShape()):
                        lastPoint=path[i]
                        line=None
                        current=i
                        counter=0
                        points.append((lastPoint[0]*self.CELL_SIZE+self.OFFSET,lastPoint[1]*self.CELL_SIZE+self.OFFSET))
                        break
            counter+=1
        points.append((path[-1][0]*self.CELL_SIZE+self.OFFSET,path[-1][1]*self.CELL_SIZE+self.OFFSET))
        return points

    def angularDistance(self,pathPoint):
        # https://fr.wikihow.com/calculer-l%E2%80%99angle-entre-deux-vecteurs

        currentPosition=(self._robot.getPose().getX(),self._robot.getPose().getY())
        dx = pathPoint[0]-currentPosition[0]
        dy = pathPoint[1]-currentPosition[1]

        delta_degrees=2 # turn right
        v1 = (sin(-radians(self._robot.getPose().getOrientation())),cos(-radians(self._robot.getPose().getOrientation()))) # norm 1
        v1_delta = (sin(-radians(self._robot.getPose().getOrientation()+delta_degrees)),cos(-radians(self._robot.getPose().getOrientation()+delta_degrees)))
        v2=(dx,dy)

        dot_product = v1[0]*v2[0]+v1[1]*v2[1]
        dot_product_delta = v1_delta[0]*v2[0]+v1_delta[1]*v2[1]
        norm_v2=(v2[0]**2+v2[1]**2)**0.5

        theta = acos(dot_product/norm_v2)
        theta_delta = acos(dot_product_delta/norm_v2)

        return degrees(theta) * (1 if degrees(theta)-degrees(theta_delta)>0 else -1)


