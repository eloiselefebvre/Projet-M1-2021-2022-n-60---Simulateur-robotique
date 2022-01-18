from robotSimulator.robots.Robot import Robot
from robotSimulator.Rectangle import Rectangle
from robotSimulator.Representation import Representation
from robotSimulator.actuators.Wheel import Wheel

class TwoWheelsRobot(Robot):

    def __init__(self,xPos,yPos,orientation,robotWidth=50,robotHeight=60,wheelsRadius=10,distanceBetweenWheels=50):
        super().__init__(xPos,yPos,orientation,Representation(Rectangle(robotWidth,robotHeight,"#0F0",3)))
        self._width = 100
        self._radius = 50
        robotCenter = robotWidth/2;
        self._leftWheel = Wheel(robotCenter-distanceBetweenWheels/2, robotHeight/2-wheelsRadius, wheelsRadius, 8)
        self._rightWheel = Wheel(robotCenter+distanceBetweenWheels/2-8, robotHeight/2-wheelsRadius, wheelsRadius, 8)
        self.addComponent(self._leftWheel)
        self.addComponent(self._rightWheel)

    def setLeftWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed);

    def setRightWheelSpeed(self,speed):
        self._leftWheel.setSpeed(speed);