from Robot import Robot

class FourWheelsRobot(Robot):

    def __init__(self,speed,x,y,width,height,orientation):
        Robot.__init__(self,x,y,width,height,orientation)
        self._firstWheelSpeed = speed

    def setLeftFrontWheelSpeed(self,speed):
        self._leftWheelSpeed = speed

    def setRightFrontWheelSpeed(self,speed):
        self._rightWheelSpeed = speed

    def setLeftBackWheelSpeed(self,speed):
        self._leftWheelSpeed = speed

    def setRightBackWheelSpeed(self,speed):
        self._rightWheelSpeed = speed

