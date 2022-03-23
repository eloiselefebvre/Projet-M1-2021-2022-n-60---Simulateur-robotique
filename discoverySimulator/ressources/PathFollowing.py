from math import sqrt, sin, radians, cos, degrees, acos

from PyQt5.QtCore import QPointF

from discoverySimulator.ressources.PathFinding import PathFinding
from discoverySimulator.robots import TwoWheelsRobot


class PathFollowing():

    FORWARD_SPEED = 200
    TURN_SPEED = 100

    def __init__(self,environment,robot,path):
        self._robot = robot
        self._environment=environment
        self._path = path
        self._path.setEndPoint(QPointF(500,500))
        self._nextPointIndex = 0
        self._modifyOrientation = True


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

    def followSimplifyPath(self):
        if self._robot.isFollowingPath():
            distance = sqrt((self._path.getSimplifiedPath()[self._nextPointIndex][0] - self._robot.getPose().getX()) ** 2 + (self._path.getSimplifiedPath()[self._nextPointIndex][1] - self._robot.getPose().getY()) ** 2)
            angularDistance = self.angularDistance(self._path.getSimplifiedPath()[self._nextPointIndex])
            if (angularDistance > 1 or angularDistance < -1) and self._modifyOrientation:  # TODO : Attention aux déviations sur les longues distances ! -> Algo de suivi de ligne ?
                if angularDistance < 0:
                    self._robot.setRightWheelSpeed(-self.TURN_SPEED)
                    self._robot.setLeftWheelSpeed(self.TURN_SPEED)
                else:
                    self._robot.setRightWheelSpeed(self.TURN_SPEED)
                    self._robot.setLeftWheelSpeed(-self.TURN_SPEED)
            else:
                self._modifyOrientation = False
            if distance > 10 and not self._modifyOrientation:
                self._robot.setRightWheelSpeed(self.FORWARD_SPEED)
                self._robot.setLeftWheelSpeed(self.FORWARD_SPEED)
            else:
                if not self._modifyOrientation:
                    self._nextPointIndex += 1
                self._modifyOrientation = True
            if self._nextPointIndex == len(self._path.getSimplifiedPath()):
                self._robot.setRightWheelSpeed(0)
                self._robot.setLeftWheelSpeed(0)
                self._robot.setIsFollowingPath(False)