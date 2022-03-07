from random import random

from robotSimulator import Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line, Point
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.simulation import Simulation, Environment
import time


def reinforcementLearningTest():

    robot = TwoWheelsRobot()
    robot.setRightWheelSpeed(500)
    robot.setLeftWheelSpeed(300)

    env = Environment(1500, 1500)
    env.addObject(robot,500,500,0)
    sim = Simulation(env)
    start = sim.time()

    for i in range(100):
        for j in range(100):
            env.addVirtualObject(Object(Representation(Line(1500,1,"#f00"))),i*15,0)
            env.addVirtualObject(Object(Representation(Line(1500,1,"#f00"))),0,j*15,-90)

    robotPoseX=robot.getPose().getX()
    robotPoseY=robot.getPose().getY()
    robotCenter=Point(robotPoseX,robotPoseY)

    Q = []

    testTime=5

    sim.run()
    sim.showInterface()

    while True:
        current = sim.time()
        if current<testTime:
            # print(current)
            if current - start > 1:
                start = current
        time.sleep(.01)

