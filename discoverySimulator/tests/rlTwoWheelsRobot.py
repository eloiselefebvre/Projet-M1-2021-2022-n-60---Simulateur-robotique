import time

from discoverySimulator.ressources.RL import RL
from discoverySimulator.robots import CircularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

from discoverySimulator.ressources.pretrainedRLQTables import goForwardTwoWheelsRobot

def reinforcementLearningTest():

    env=Environment(1500,1500)
    robot=CircularTwoWheelsRobot()
    env.addObject(robot,500,400,-90)

    actionBuilders = [
        {
            "id":robot.getLeftWheel().getID(),
            "getter": robot.getLeftWheel().getSpeed,
            "setter": robot.getLeftWheel().setSpeed,
            "min": 0,
            "max": 600,
            "intervals":2
        },
        {
            "id":robot.getRightWheel().getID(),
            "getter": robot.getRightWheel().getSpeed,
            "setter": robot.getRightWheel().setSpeed,
            "min": 0,
            "max": 600,
            "intervals":2
        }
    ]

    spaceBuilders = [
        {"id":robot.getLeftWheel().getID()},
        {"id":robot.getRightWheel().getID()}
    ]

    rl = RL(actionBuilders,spaceBuilders,QTable=goForwardTwoWheelsRobot)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    initialPose = robot.getPose().copy()

    learningTime = 6
    start = sim.time()

    # while True:
    #     current = sim.time()
    #     if current - start < learningTime:
    #         startPosition = (robot.getPose().getX(), robot.getPose().getY())
    #         startOrientation = robot.getPose().getOrientation()
    #         startOrientation %= 360
    #
    #         # action during 0.1 second to see the result of the action
    #         rl.execute()
    #
    #         time.sleep(0.1)
    #
    #         endPosition = (robot.getPose().getX(), robot.getPose().getY())
    #         endOrientation = robot.getPose().getOrientation()
    #
    #         distance = ((endPosition[0] - startPosition[0]) ** 2 + (endPosition[1] - startPosition[1]) ** 2)**0.5
    #
    #         reward = distance / (1 + (endOrientation - startOrientation) ** 2)  # encourages to go straight
    #         # reward = (endOrientation-startOrientation)/(distance+1) # encourages to turn
    #         rl.learn(reward)
    #
    #     else:
    #         start = sim.time()
    #         robot.setPose(initialPose.copy())
    #         robot.setLeftWheelSpeed(0)
    #         robot.setRightWheelSpeed(0)
    #         robot.setCollidedState(False)
    #         rl.reset()
    #
    #     time.sleep(.01)

    # pretrained table
    while True:
        rl.execute()
        time.sleep(.01)







