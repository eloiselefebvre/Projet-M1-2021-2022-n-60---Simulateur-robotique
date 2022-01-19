from robotSimulator.robots.Robot import Robot
from robotSimulator.Rectangle import Rectangle
from robotSimulator.Representation import Representation
from robotSimulator.actuators.Wheel import Wheel

class TwoWheelsRobot(Robot):

    def __init__(self,x,y,orientation,robotWidth=50,robotHeight=60,wheelsRadius=10,distanceBetweenWheels=50):
        rep=Rectangle(robotWidth,robotHeight,"#0F0",3)
        super().__init__(x,y,orientation,Representation(rep))
        self._width = 100
        self._radius = 50
        self._leftWheel = Wheel(-distanceBetweenWheels/2+4,0, wheelsRadius, 8)
        self._rightWheel = Wheel(distanceBetweenWheels/2-4,0, wheelsRadius, 8)
        self.addComponent(self._leftWheel)
        self.addComponent(self._rightWheel)

    def setLeftWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed)