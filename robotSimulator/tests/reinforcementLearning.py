import time
from math import sqrt

from robotSimulator.ressources.ReinforcementLearning import ReinforcementLearning
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.simulation import Environment, Simulation


def reinforcementLearningTest():

    env=Environment(1500,1500)
    robot=TwoWheelsRobot()
    env.addObject(robot,200,400,-90)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    startPosition = (robot.getPose().getX(),robot.getPose().getY())
    startOrientation = robot.getPose().getOrientation()
    currentState = (robot.getLeftWheel().getSpeed(), robot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState)
    previousDistance=0
    distanceMax=0

    timeLearning = 5
    start=sim.time()

    while True:

        current=sim.time()
        if current-start<timeLearning:
            currentPosition=(robot.getPose().getX(),robot.getPose().getY())
            action = reinforcementLearning.getActionToExecute()
            distance = sqrt((currentPosition[0]-startPosition[0])**2+(currentPosition[1]+startPosition[1]**2))

            robot.setRightWheelSpeed(robot.getRightWheel().getSpeed()+action[0])
            robot.setLeftWheelSpeed(robot.getLeftWheel().getSpeed()+action[1])

            if distance>distanceMax:
                distanceMax=distance
                reinforcementLearning.executedActionFeedback(3)
            elif distance>previousDistance:
                reinforcementLearning.executedActionFeedback(1)
            else :
                reinforcementLearning.executedActionFeedback(-1)

            previousDistance=distance

        else:
            start=sim.time()
            robot.getPose().move(startPosition[0],startPosition[1])
            robot.getPose().setOrientation(startOrientation)
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
            robot.setCollidedState(False)
            previousDistance=0
            reinforcementLearning.reset()

        time.sleep(.01)


