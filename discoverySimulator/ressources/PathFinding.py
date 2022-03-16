import time
from math import sqrt, atan, degrees

from PyQt5.QtCore import QPoint

from discoverySimulator.Object import Object
from discoverySimulator.Obstacle import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Rectangle, Circle, Point


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
    FORWARD_SPEED = 200
    TURN_SPEED = 100
    CELL_SIZE = 15
    OFFSET = CELL_SIZE/2

    def __init__(self, environment, robot,NODE=None):
        self._environment=environment
        self._robot=robot

        self.__ROWS_NUMBER = (self._environment.getWidth())/15
        self.__COLS_NUMBER = (self._environment.getHeight())/15

        self.__beginNode = (10,10)
        self.__endNode = (30,30)
        self._nodes = {}
        self.createNode(self.__beginNode)
        self.setRobotStartPosition()

        self.__astar()

    def setRobotStartPosition(self):
        self._environment.addObject(self._robot,self.__beginNode[0]*15+7,self.__beginNode[1]*15+7)


    def __setBeginNode(self, node):
        if self.__getNodeValue(node) and self.__isValidNode(node):
            self.__beginNode = node
            self.__setNodeColor(self.__beginNode, self.COLORS['begin_node'])
            return True
        return False

    def __setEndNode(self, node):
        if self.__getNodeValue(node) and self.__isValidNode(node):
            self.__endNode = node
            self.__setNodeColor(self.__endNode, self.COLORS['end_node'])
            return True
        return False

    def __setNodeColor(self, node, color):
        self._nodes[node].setColor(color)

    def __getNodeValue(self, node):
        for obj in self._environment.getObjects():
            obstacle = obj.getRepresentation().getShape().offset(self._robot.getRepresentation().getShape().getWidth()/2+5)
            if isinstance(obj,Obstacle):
                if  obstacle.contains(QPoint(node[0]*15,node[1]*15)):
                    return False
                if  obstacle.contains(QPoint(node[0]*15,(node[1]+1)*15)):
                    return False
                if  obstacle.contains(QPoint((node[0]+1)*15,node[1]*15)):
                    return False
                if  obstacle.contains(QPoint((node[0]+1)*15,(node[1]+1)*15)):
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
            time.sleep(0.01)
            closed_nodes[current] = opened_nodes.pop(current)
            opened_nodes_heuristic.pop(current)
            self.__setNodeColor(current, self.COLORS['closed_node'])
            neighbors = self.__getNodeNeighbors(current)
            for n in neighbors:
                weight = 0
                for ne in self.__getNodeNeighbors(n):
                    if not self.__getNodeValue(ne):
                        weight = 2
                        break
                if not n in closed_nodes and self.__getNodeValue(n):
                    distanceFromBeginNode = closed_nodes[current] + 1 + weight
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
        self.__setNodeColor(self.__endNode,self.COLORS["end_node"])
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        for p in path:
            self.__setNodeColor(p, self.COLORS["path_node"])
        self.goTo(path)
        # self.goToWithFuzzyLogic(path)

    def __heuristic(self, node):
        return self.__euclidDistanceToEnd(node)

    def __manhattanDistanceToEnd(self, node):
        return abs(self.__endNode[0] - node[0]) + abs(self.__endNode[1] - node[1])

    def __euclidDistanceToEnd(self, node):
        return ((self.__endNode[0] - node[0]) ** 2 + (self.__endNode[1] - node[1]) ** 2) ** 0.5

    def createNode(self,node):
        self._nodes[node]=Rectangle(15, 15, "#FF9900")
        self._environment.addVirtualObject(Object(Representation(self._nodes[node])),node[0]*self.CELL_SIZE+self.OFFSET,node[1]*self.CELL_SIZE+self.OFFSET)

    def refreshPath(self,sender):
        self.__astar()

    def goTo(self,path):
        pathPoints = [(p[0]*self.CELL_SIZE+self.OFFSET,p[1]*self.CELL_SIZE+self.OFFSET) for i,p in enumerate(path) if i % 5 == 0]
        del pathPoints[0]
        for i in range (len(pathPoints)):
            distance = sqrt((pathPoints[i][0]-self._robot.getPose().getX())**2+(pathPoints[i][1]-self._robot.getPose().getY())**2)
            angularDistance = self.angularDistance(pathPoints[i])
            while angularDistance>5 or angularDistance<-5:
                if angularDistance < -5:
                    self._robot.setRightWheelSpeed(self.TURN_SPEED)
                    self._robot.setLeftWheelSpeed(-self.TURN_SPEED)
                elif angularDistance > 5:
                    self._robot.setRightWheelSpeed(-self.TURN_SPEED)
                    self._robot.setLeftWheelSpeed(self.TURN_SPEED)
                angularDistance = self.angularDistance(pathPoints[i])
            while distance > 10:
                self._robot.setRightWheelSpeed(self.FORWARD_SPEED)
                self._robot.setLeftWheelSpeed(self.FORWARD_SPEED)
                distance = sqrt((pathPoints[i][0] - self._robot.getPose().getX()) ** 2 + (pathPoints[i][1] - self._robot.getPose().getY()) ** 2)


    def goToWithFuzzyLogic(self,path):

        pointADroite=[]
        pointAGauche=[]
        offset=20
        rightTurnRightWheel=[0 for _ in range(11)]
        rightTurnLeftWheel = [0 for _ in range(11)]
        leftTurnRightWheel = [0 for _ in range(11)]
        leftTurnLeftWheel = [0 for _ in range(11)]
        pathPoints = [(p[0] * self.CELL_SIZE + self.OFFSET, p[1] * self.CELL_SIZE + self.OFFSET) for i, p in enumerate(path) if i % 10 == 0]
        del pathPoints[0]

        for i in range(150):
            pointADroite.append(0)
        for i in range(150,190):
            pointADroite.append(i*(1/2)+5)
        for i in range(190,270):
            pointADroite.append(i*(10/9))
        for i in range(270,361):
            pointADroite.append(i*(-2/9)+120)

        for i in range(90):
            pointAGauche.append(i*(2/9)+120)
        for i in range(90,170):
            pointAGauche.append(i*(-10/9))
        for i in range(170,220):
            pointAGauche.append(i*(-1/2)+5)
        for i in range(220,361):
            pointAGauche.append(0)

        for i in range(-5, 6):
            if i <= 0:
                rightTurnRightWheel[i + 5] = 0
            else:
                rightTurnRightWheel[i + 5] =  int(i * (5/18) + 50/3)
            leftTurnLeftWheel[i + 5] = rightTurnRightWheel[i + 5]
        for i in range(-5, 6):
            if i >= 0:
                rightTurnLeftWheel[i + 5] = 0
            else:
                rightTurnLeftWheel[i + 5] = int(i * (-5/18) + 50/3)
            leftTurnRightWheel[i + 5] = rightTurnLeftWheel[i + 5]


        for index in range (len(pathPoints)):
            distance = sqrt((pathPoints[index][0] - self._robot.getPose().getX()) ** 2 + (pathPoints[index][1] - self._robot.getPose().getY()) ** 2)

            while (self._robot.getPose().getX()<=pathPoints[index][0]-offset or self._robot.getPose().getX()>=pathPoints[index][0]+offset or self._robot.getPose().getY()>=pathPoints[index][1]-offset or self._robot.getPose().getY()<=pathPoints[index][1]+offset) and distance>=20:
                distance = sqrt((pathPoints[index][0] - self._robot.getPose().getX()) ** 2 + (pathPoints[index][1] - self._robot.getPose().getY()) ** 2)
                print("distance",distance)
                angularDistance = self.angularDistance(pathPoints[index])

                pointADroiteValue = pointADroite[int(angularDistance)]
                pointAGaucheValue = pointAGauche[int(angularDistance)]
                print('angle',angularDistance)

                numerator = 0
                denominator = 0

                #right wheel
                for x in range(11):
                    print("right")

                    cutValueRightPoint = min(pointADroiteValue,rightTurnRightWheel[x])
                    cutValueLeftPoint = min(pointAGaucheValue,leftTurnRightWheel[x])

                    numerator += (x+5)*(cutValueRightPoint+cutValueLeftPoint)
                    denominator += (cutValueLeftPoint+cutValueRightPoint)

                    if denominator!=0:
                        gravity=numerator/denominator
                    else:
                        gravity=100
                    self._robot.setRightWheelSpeed(gravity)
                    distance = sqrt((pathPoints[index][0] - self._robot.getPose().getX()) ** 2 + (pathPoints[index][1] - self._robot.getPose().getY()) ** 2)

                numerator=0
                denominator=0

                #left wheel
                for x in range(11):

                    cutValueRightPoint = min(pointADroiteValue, rightTurnLeftWheel[x])
                    cutValueLeftPoint = min(pointAGaucheValue, leftTurnLeftWheel[x])

                    numerator += (x + 5) * (cutValueRightPoint + cutValueLeftPoint)
                    denominator += (cutValueLeftPoint + cutValueRightPoint)

                    if denominator != 0:
                        gravity = numerator / denominator
                    else:
                        gravity = 100
                    self._robot.setLeftWheelSpeed(gravity)

                    time.sleep(.01)
                    distance = sqrt((pathPoints[index][0] - self._robot.getPose().getX()) ** 2 + (pathPoints[index][1] - self._robot.getPose().getY()) ** 2)

            print("next point >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


    def angularDistance(self,pathPoint):
        currentPosition=(self._robot.getPose().getX(),self._robot.getPose().getY())
        dx = pathPoint[0]-currentPosition[0]
        dy = pathPoint[1]-currentPosition[1]
        theta = atan(dx/dy)
        if self._robot.getPose().getOrientation() <= 180 - degrees(theta):
            angularDistance = -(self._robot.getPose().getOrientation() + degrees(theta))
        elif self._robot.getPose().getOrientation()>360-degrees(theta):
            angularDistance = -((self._robot.getPose().getOrientation()-360)+degrees(theta))
        else:
            angularDistance = 360-(self._robot.getPose().getOrientation()) + degrees(theta)
        return angularDistance


