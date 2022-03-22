import time
from math import sqrt
from discoverySimulator import Pose
from discoverySimulator.ressources.ReinforcementLearningMSO import ReinforcementLearning
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

def reinforcementLearningTest():

    env=Environment(1500,1500)
    robot=RectangularTwoWheelsRobot()
    env.addObject(robot,500,400,-90)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    initPosition = (robot.getPose().getX(),robot.getPose().getY())
    initOrientation = robot.getPose().getOrientation()

    currentState = (robot.getLeftWheel().getSpeed(), robot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState)


    # MSO TODO : le temps simulé avec un facteur 1 parait plus lent que le temps réel  -> normal ?
    timeLearning = 5
    start=sim.time()


    while True:

        current=sim.time()
        if current-start<timeLearning:
            currentState = reinforcementLearning.getState()
            startPosition=(robot.getPose().getX(),robot.getPose().getY())
            startOrientation = robot.getPose().getOrientation()

            if startOrientation < 0:
                startOrientation = 360 + startOrientation

            # application de l'action pendant 0.1 secondes
            action = reinforcementLearning.getActionToExecute()

            robot.setRightWheelSpeed(robot.getRightWheel().getSpeed()+action[0])
            robot.setLeftWheelSpeed(robot.getLeftWheel().getSpeed()+action[1])

            #print("avant", robot.getPose().getX(), robot.getPose().getY(), robot.getPose().getOrientation())
            time.sleep(0.1)
            #print("après", robot.getPose().getX(), robot.getPose().getY(), robot.getPose().getOrientation())
            endPosition=(robot.getPose().getX(),robot.getPose().getY())
            endOrientation = robot.getPose().getOrientation()

            if endOrientation < 0:
                endOrientation = 360 + endOrientation

            distance = sqrt((endPosition[0]-startPosition[0])**2+(endPosition[1]-startPosition[1])**2)

            reward = distance / (1 + (endOrientation-startOrientation)**2)     # incite à aller tout droit
            # reward = (endOrientation-startOrientation)/(distance+1)             # inclite à tourner sur soi-même

            # print(currentState, action, distance, startOrientation, endOrientation, reward)

            reinforcementLearning.learn(reward)

        else:
            start=sim.time()
            robot.getPose().move(initPosition[0],initPosition[1])
            robot.getPose().setOrientation(initOrientation)
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
            robot.setCollidedState(False)
            robot.setOdometryPose(Pose(initPosition[0],initPosition[1],initOrientation))
            reinforcementLearning.reset()

        time.sleep(.05)


