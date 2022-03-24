from discoverySimulator import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes.Polygon import Polygon
from discoverySimulator.ressources.PathFinding import PathFinding
from discoverySimulator.ressources.PathFollowing import PathFollowing
from discoverySimulator.robots import FourWheelsRobot, CircularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

def aStar():

    env=Environment(1500,1500)
    robot = CircularTwoWheelsRobot()
    # robot = FourWheelsRobot()
    pol=Polygon([(200,200),(300,200),(400,300),(300,350),(250,300)],"#f0f")
    # pol=Polygon([(200,200),(400,400),(200,400)],"#f0f")
    obs=Obstacle(Representation(pol))
    env.addObject(robot,100,100,90)
    env.addObject(obs)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    pathFinding = PathFinding(env,robot.getBoundingWidth(),True,0)
    pathFollowing=PathFollowing(robot)

    pathFinding.findPath((robot.getPose().getX(),robot.getPose().getY()),(600,500),pathFollowing.startFollowing)

