from math import cos,sin,radians,degrees

from robotSimulator.robots.Robot import Robot
from robotSimulator.representation.shapes.Rectangle import Rectangle
from robotSimulator.representation.Representation import Representation
from robotSimulator.actuators.Wheel import Wheel

import random

class TwoWheelsRobot(Robot):

    DEFAULT_WHEEL_WIDTH = 8
    DEFAULT_BORDER_RADIUS = 3
    COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]

    def __init__(self,x,y,orientation,robotWidth=50,robotHeight=60,distanceBetweenWheels=50,wheelsRadius=10):
        rep=Rectangle(robotWidth,robotHeight,random.choice(self.COLORS),self.DEFAULT_BORDER_RADIUS)
        super().__init__(x,y,orientation,Representation(rep))
        self._leftWheel = Wheel(-distanceBetweenWheels/2+4,0, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self._rightWheel = Wheel(distanceBetweenWheels/2-4,0, wheelsRadius, self.DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftWheel)
        self.addComponent(self._rightWheel)
        self._distanceBetweenWheels = distanceBetweenWheels


    def move(self):
        # vitesse élémentaire
        rightElementarySpeed = self._rightWheel.getRadius() * self._rightWheel.getSpeed()
        leftElementarySpeed = self._leftWheel.getRadius() * self._leftWheel.getSpeed()

        # vitesse moyenne du robot
        averageSpeedRobot = (rightElementarySpeed + leftElementarySpeed) / 2

        # vitesse le long des axes x et y
        Phi = radians(self._orientation + 90)
        dx = averageSpeedRobot * cos(Phi)
        dy = averageSpeedRobot * sin(Phi)

        # vitesse angulaire
        dPhi = degrees((rightElementarySpeed - leftElementarySpeed)/(2*self._distanceBetweenWheels))

        self._pos.move(self._pos.getX() + dx, self._pos.getY() + dy)
        self._orientation += dPhi

        self._representation.setParameters(self._pos,self._orientation)

    def setLeftWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed):
        self._rightWheel.setSpeed(speed)
