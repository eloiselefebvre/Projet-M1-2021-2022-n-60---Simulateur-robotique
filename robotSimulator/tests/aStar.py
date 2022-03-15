from robotSimulator import Obstacle
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Circle
from robotSimulator.ressources.PathFinding import PathFinding
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.simulation import Environment, Simulation

def aStar():

    env=Environment(1500,1500)
    robot = TwoWheelsRobot()
    obs=Obstacle(Representation(Circle(50,"#f00")))
    env.addObject(obs,250,250)
    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    PathFinding(env,robot)

