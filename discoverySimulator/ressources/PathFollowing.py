from math import sqrt, sin, radians, cos, degrees, acos

from discoverySimulator.robots import Robot


class PathFollowing():

    """ The PathFollowing class provides a path following for a robot."""

    MAX_FORWARD_SPEED = 500
    MIN_FORWARD_SPEED = 300
    MIN_DISTANCE_FOR_MAX_FORWARD_SPEED = 60.0
    TURN_SPEED_FACTOR = 10
    DISTANCE_FOR_NEXT_POINT = 30
    DISTANCE_FOR_END_POINT = 5

    def __init__(self,robot):
        """ Constructs a following path.
        @param robot  Robot who will follow the path
        """
        self._robot = robot
        for wheel in self._robot.getWheels():
            wheel.setSpeed(0)
        self._robot.setSpeedLock(True)
        self._path = None
        self._nextPointIndex = 0
        self._modifyOrientation = True

    # GETTERS
    def getRobot(self) -> Robot:
        """ Returns the robot who follow the path."""
        return self._robot

    def angularDistance(self,pathPoint) -> float:
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

        return degrees(theta) * (-1 if degrees(theta)-degrees(theta_delta)>0 else 1)

    def startFollowing(self,path):
        if path is not None:
            self._path=path
            self._robot.setPathFollowing(self)

    def followPath(self):
        if self._path is not None:
            distance = sqrt((self._path[self._nextPointIndex][0]-self._robot.getPose().getX())**2+(self._path[self._nextPointIndex][1]-self._robot.getPose().getY())**2)
            angularDistance = self.angularDistance(self._path[self._nextPointIndex])
            if (0<angularDistance<2 or 0>angularDistance>-2) and self._modifyOrientation:
                self._modifyOrientation=False

            f = min(PathFollowing.MIN_DISTANCE_FOR_MAX_FORWARD_SPEED,distance) / PathFollowing.MIN_DISTANCE_FOR_MAX_FORWARD_SPEED
            baseSpeed=max(PathFollowing.MAX_FORWARD_SPEED*f,PathFollowing.MIN_FORWARD_SPEED)/(abs(angularDistance)/(PathFollowing.TURN_SPEED_FACTOR if not self._modifyOrientation else 1)+1)
            self._robot.setSpeedLock(False)
            self._robot.setRightWheelSpeed(baseSpeed + PathFollowing.TURN_SPEED_FACTOR * angularDistance)
            self._robot.setLeftWheelSpeed(baseSpeed - PathFollowing.TURN_SPEED_FACTOR * angularDistance)
            self._robot.setSpeedLock(True)

            if (distance<PathFollowing.DISTANCE_FOR_NEXT_POINT and self._nextPointIndex<len(self._path)-1) \
                or (distance<PathFollowing.DISTANCE_FOR_END_POINT and self._nextPointIndex==len(self._path)-1):
                self._nextPointIndex+=1

            if self._nextPointIndex==len(self._path):
                self._robot.setSpeedLock(False)
                self._robot.setRightWheelSpeed(0)
                self._robot.setLeftWheelSpeed(0)
                self._robot.setPathFollowing(None)
