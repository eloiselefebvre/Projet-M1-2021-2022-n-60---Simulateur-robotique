import time

from discoverySimulator.ressources.RL import RL
from discoverySimulator.robots import FourWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

from discoverySimulator.ressources.pretrainedRLQTables import goForwardTwoWheelsRobot

def reinforcementLearningTest():

    env=Environment(1500,1500)
    robot=FourWheelsRobot()
    env.addObject(robot,100,750,-90)

    actionBuilders = [
        {
            "id":robot.getFrontLeftWheel().getID(),
            "getter": robot.getFrontLeftWheel().getSpeed,
            "setter": robot.getFrontLeftWheel().setSpeed,
            "min": 0,
            "max": 600,
            "intervals":2
        },
        {
            "id":robot.getFrontRightWheel().getID(),
            "getter": robot.getFrontRightWheel().getSpeed,
            "setter": robot.getFrontRightWheel().setSpeed,
            "min": 0,
            "max": 600,
            "intervals":2
        },
        {
            "id": robot.getBackLeftWheel().getID(),
            "getter": robot.getBackLeftWheel().getSpeed,
            "setter": robot.getBackLeftWheel().setSpeed,
            "min": 0,
            "max": 600,
            "intervals": 2
        },
        {
            "id":robot.getBackRightWheel().getID(),
            "getter": robot.getBackRightWheel().getSpeed,
            "setter": robot.getBackRightWheel().setSpeed,
            "min": 0,
            "max": 600,
            "intervals":2
        }
    ]

    spaceBuilders = [
        {"id":robot.getFrontLeftWheel().getID()},
        {"id":robot.getFrontRightWheel().getID()},
        {"id": robot.getBackLeftWheel().getID()},
        {"id": robot.getBackRightWheel().getID()}
    ]

    rl = RL(actionBuilders,spaceBuilders,{
        "explorationRateDecrease":0.9999
    })

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    initialPose = robot.getPose().copy()

    learningTime = 6
    start = sim.time()

    while True:
        current = sim.time()
        if current - start < learningTime:
            startPosition = (robot.getPose().getX(), robot.getPose().getY())
            startOrientation = robot.getPose().getOrientation()
            startOrientation %= 360

            # action during 0.1 second to see the result of the action
            rl.execute()

            time.sleep(0.1)

            endPosition = (robot.getPose().getX(), robot.getPose().getY())
            endOrientation = robot.getPose().getOrientation()

            distance = ((endPosition[0] - startPosition[0]) ** 2 + (endPosition[1] - startPosition[1]) ** 2)**0.5

            reward = distance / (1 + (endOrientation - startOrientation) ** 2)  # encourages to go straight
            # reward = (endOrientation-startOrientation)/(distance+1) # encourages to turn
            rl.learn(reward)

        else:
            start = sim.time()
            robot.setPose(initialPose.copy())
            robot.setFrontLeftWheelSpeed(0)
            robot.setFrontRightWheelSpeed(0)
            robot.setBackLeftWheelSpeed(0)
            robot.setBackRightWheelSpeed(0)
            robot.setCollidedState(False)
            rl.reset()

        time.sleep(.01)

    # # pretrained table
    # while True:
    #     rl.execute()
    #     time.sleep(.01)







