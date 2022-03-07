from math import cos, pi, sin, radians, degrees

from robotSimulator import Object
from robotSimulator.config import config
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Point, Rectangle


class Odometry: # TODO : Tout remettre dans TwoWheelsRobot et surcharger dans FourWheelsRobot

    ODOMETRY_COLOR = "#8B86AC"

    def __init__(self,robot,env):
        self._robot = robot
        self._env = env
        self._counter=0
        self._odom=[]

        self._x = self._robot.getPose().getX()
        self._y = self._robot.getPose().getY()
        self._teta = -self._robot.getPose().getOrientation()

        robotShape = self._robot.getRepresentation().getShape()
        self._midWidthRobot = robotShape.getWidth()/2 if isinstance(robotShape,Rectangle) else robotShape.radius() + self._robot.getPose().getRotX() # TODO : Voir pour robot non rectange et non cercle

    def odometry(self):
        vd = self._robot.getRightLinearSpeed()
        vg = self._robot.getLeftLinearSpeed()
        v = (vd + vg) / 2
        e = self._robot.getDistanceBetweenWheels()
        d = v * config["time_step"]/60
        if vd != vg:
            R = e * (vd + vg)/ (vd - vg)
            if R!=0:
                # calcul des paramètres du cercle trajectoire
                x0 = self._x + R * cos(-radians(self._teta))
                y0 = self._y + R * sin(-radians(self._teta))
                # calcul position du robot
                d_teta = d/R
                self._teta += degrees(d_teta)
                self._x = x0 - R * cos(-radians(self._teta))
                self._y = y0 - R * sin(-radians(self._teta))
        else:
            self._x-=d*sin(-radians(self._teta))
            self._y-=d*cos(-radians(self._teta))

        if self._robot.getDrawOdometry():
            self.drawOdometry()

    def drawOdometry(self):
        new_Point = Point(int(self._x), int(self._y), self.ODOMETRY_COLOR)

        if self._counter == 0:
            self._odom.append(Object(Representation(new_Point)))
            self._env.addVirtualObject(self._odom[-1])
        self._counter = (self._counter + 1) % 15

    def hideOdometry(self):
        for point in self._odom:
            self._env.removeVirtualObject(point)
        self._robot.setDrawOdometry()