# from robotSimulator.robots.TwoWheelsRobot import TwoWheelsRobot
# from robotSimulator.robots.FourWheelsRobot import FourWheelsRobot

class Odometry:

    def __init__(self,robot):
        self._robot = robot
        #
        # self._initialePositionX = self._robot.getPose().getX()
        # self._initialePositionY = self._robot.getPose().getY()
        # self._initialeOrientation = self._robot.getPose().getOrientation()

        # if isinstance(self._robot,TwoWheelsRobot):
        #     self.odometryTwoWheelsRobots()
        # if isinstance(self._robot,FourWheelsRobot):
        #     self.odometryFourWheelsRobot()

    def odometryTwoWheelsRobots(self):
        self._rightWheelSpeed = self._robot.getRightWheel().getSpeed()
        self._leftWheelSpeed = self._robot.getLeftWheel().getSpeed()
        # print("X",self._initialePositionX,"Y",self._initialePositionY)


    def odometryFourWheelsRobot(self):
        pass







