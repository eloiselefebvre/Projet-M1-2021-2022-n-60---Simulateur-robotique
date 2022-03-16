from PyQt5.QtCore import QPoint

from discoverySimulator import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle
from discoverySimulator.representation.shapes.Polygon import Polygon
from discoverySimulator.ressources.PathFinding import PathFinding
from discoverySimulator.robots import TwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

# utiliser la fonction goToWithFuzzyLogic dans PathFinding

def aStarWithFuzzyLogic():

    env=Environment(1500,1500)
    robot = TwoWheelsRobot()
    obs=Obstacle(Representation(Circle(70,"#f00")))
    # env.addObject(obs,300,300)
    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    PathFinding(env,robot)

