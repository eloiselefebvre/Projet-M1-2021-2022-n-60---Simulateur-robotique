import time
from math import sqrt, cos, radians

from discoverySimulator import Pose
from discoverySimulator.ressources.ReinforcementLearning import ReinforcementLearning
from discoverySimulator.robots import RectangleTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation


def reinforcementLearningTest():

    env=Environment(1500,1500)
    robot=RectangleTwoWheelsRobot()
    env.addObject(robot,500,400,-90)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    startPosition = (robot.getPose().getX(),robot.getPose().getY())
    startOrientation = robot.getPose().getOrientation()
    previousPosition = startPosition
    previousOrientation=startOrientation

    if startOrientation<0:
        startOrientation=360+startOrientation
    currentState = (robot.getLeftWheel().getSpeed(), robot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState)

    timeLearning = 6
    start=sim.time()

    while True:

        current=sim.time()
        if current-start<timeLearning:
            currentPosition=(robot.getPose().getX(),robot.getPose().getY())

            currentOrientation = robot.getPose().getOrientation()

            action = reinforcementLearning.getActionToExecute()

            distance = sqrt((currentPosition[0]-previousPosition[0])**2+(currentPosition[1]-previousPosition[1])**2)
            product = distance * cos(radians(currentOrientation-previousOrientation))

            robot.setRightWheelSpeed(robot.getRightWheel().getSpeed()+action[0])
            robot.setLeftWheelSpeed(robot.getLeftWheel().getSpeed()+action[1])

            reinforcementLearning.executedActionFeedback(product)

        else:
            start=sim.time()
            robot.getPose().move(startPosition[0],startPosition[1])
            robot.getPose().setOrientation(startOrientation)
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
            robot.setCollidedState(False)
            robot.setOdometryPose(Pose(startPosition[0],startPosition[1],startOrientation))
            reinforcementLearning.reset()

        time.sleep(.01)


