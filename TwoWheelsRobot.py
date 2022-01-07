from Rectangle import Rectangle
from Robot import Robot
from Wheel import Wheel


class TwoWheelsRobot(Robot):

    def __init__(self,x,y,width,height,orientation):
        Robot.__init__(self,x,y,width,height,orientation)

        self._wheelSet.append(Wheel(10,Rectangle(0,0,8,20,0,"#1C1E32")))

    def setLeftWheelSpeed(self,speed):
        self._leftWheelSpeed = speed

    def setRightWheelSpeed(self,speed):
        self._rightWheelSpeed = speed