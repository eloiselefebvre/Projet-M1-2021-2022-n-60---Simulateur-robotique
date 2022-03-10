from robotSimulator import Obstacle
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Circle
from robotSimulator.ressources.PathFinding import PathFinding
from robotSimulator.simulation import Environment, Simulation

def aStar():

    env=Environment(1500,1500)
    obs=Obstacle(Representation(Circle(50,"#f00")))
    env.addObject(obs,250,250)
    # obs1=Obstacle(Representation(Rectangle(100,40,"#545")))
    # env.addObject(obs1,400,400)
    # obs2 = Obstacle(Representation(Polygon([QPoint(400,406),QPoint(800,810),QPoint(100,800)], "#545")))
    # env.addObject(obs2)
    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    PathFinding(env)


