import time
from PyQt5.QtCore import QPointF
from discoverySimulator import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes.Polygon import Polygon
from discoverySimulator.ressources.PathFinding import PathFinding
from discoverySimulator.robots.CircularTwoWheelsRobot import CircularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

def aStar():

    env=Environment(1500,1500)
    robot = CircularTwoWheelsRobot()
    pol=Polygon([(200,200),(300,200),(400,300),(300,350),(250,300)],"#f0f")
    obs=Obstacle(Representation(pol))
    env.addObject(robot,100,100)
    env.addObject(obs)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    pathFinding = PathFinding(env,robot,True,0)
    pathFinding.setEndPoint(QPointF(400,400))

    while True:
        pathFinding.followSimplifyPath()
        time.sleep(.01)

