from math import cos, pi, sin, radians, degrees

from robotSimulator import Object
from robotSimulator.config import config
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Point

class Odometry:

    ODOMETRY_COLOR = "#8B86AC"

    def __init__(self,robot,env):
        self._robot = robot
        self._env = env
        self._counter=0
        self._odom=[]

        self._x = self._robot.getPose().getX()
        self._y = self._robot.getPose().getY()
        self._teta = self._robot.getPose().getOrientation()

    def odometry(self):

        vd = self._robot.getRightLinearSpeed()
        vg = self._robot.getLeftLinearSpeed()

        # v = (vd + vg) / 2
        #
        L = self._robot.getDistanceBetweenWheels()
        #
        # d = v * config["time_step"]/60
        #
        # if vd != vg:
        #
        #     R = (e/2) * (vd + vg)/ (vd - vg)
        #
        #     if R!=0:
        #
        #         # calcul des paramètres du cercle trajectoire
        #         self._x = self._x - R * sin(-radians(self._teta)-pi/2)
        #         self._y0 = self._y - R * cos(-radians(self._teta)-pi/2)
        #
        #         # calcul position du robot
        #         d_teta = d/R
        #         self._teta = self._teta + degrees(d_teta)
        #         print(self._teta)
        #
        #         self._x = self._x0  + R * cos(-radians(self._teta)-pi/2)
        #         self._y = self._y0 + R * sin(-radians(self._teta)-pi/2)

        dd = vd*config["time_step"]/60
        dg = vg*config["time_step"]/60
        dcenter = (dd+dg)/2

        phi = (dd-dg)/(L*2)


        self._x = self._x+dcenter*cos(-radians(self._teta)+pi/2)
        self._y = self._y+dcenter*sin(-radians(self._teta)+pi/2)
        self._teta+=degrees(phi)

        # else:
        #     self._x+=d*sin(-radians(self._teta))
        #     self._y+=d*cos(-radians(self._teta))

        if self._robot.getDrawOdometry():
            self.drawOdometry()

    def drawOdometry(self):
        new_Point = Point(int(self._x), int(self._y), self.ODOMETRY_COLOR)
        if self._counter == 0:
            self._odom.append(Object(Representation(new_Point)))
            self._odom[-1].setZIndex(0)
            self._env.addVirtualObject(self._odom[-1])
        self._counter = (self._counter + 1) % 15

    def hideOdometry(self):
        for point in self._odom:
            self._env.removeVirtualObject(point)
        self._robot.setDrawOdometry()