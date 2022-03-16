from PyQt5.QtCore import QPoint

from robotSimulator import Obstacle
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Circle
from robotSimulator.representation.shapes.Polygon import Polygon
from robotSimulator.ressources.PathFinding import PathFinding
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.simulation import Environment, Simulation

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

