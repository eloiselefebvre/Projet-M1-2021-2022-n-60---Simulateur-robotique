from discoverySimulator.ressources.AntsColony import AntsColony
from discoverySimulator.robots.CircularTwoWheelsRobot import CircularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation


def antsColonyTest():

    env=Environment(1500,1500)
    sim=Simulation(env)
    robot=CircularTwoWheelsRobot()
    env.addObject(robot,100,100)
    robot.setRightWheelSpeed(150)
    robot.setLeftWheelSpeed(200)
    sim.run()
    sim.showInterface()
    colony=AntsColony(env)

    while True:
        colony.gridValues(robot)

