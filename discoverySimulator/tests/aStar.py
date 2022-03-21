import time

from PyQt5.QtCore import QPointF

from discoverySimulator import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle
from discoverySimulator.ressources.PathFinding import PathFinding
from discoverySimulator.robots.CircleTwoWheelsRobot import CircleTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

def aStar():

    env=Environment(1500,1500)
    robot = CircleTwoWheelsRobot()
    obs=Obstacle(Representation(Circle(50,"#f00")))
    env.addObject(robot,100,100)
    env.addObject(obs,250,250)
    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    pathFinding = PathFinding(env,robot,True)
    pathFinding.setEndPoint(QPointF(500,500))
    pathFinding.setIsFollowingPath(True)

    while True:
        pathFinding.followSimplifyPath()
        time.sleep(.01)

