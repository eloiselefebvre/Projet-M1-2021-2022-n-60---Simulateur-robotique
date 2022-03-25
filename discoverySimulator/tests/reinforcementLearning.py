import time
from math import sqrt, cos, radians
from discoverySimulator import Pose
from discoverySimulator.ressources.ReinforcementLearning import ReinforcementLearning
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

def reinforcementLearningTest():

    env=Environment(1500,1500)
    robot=RectangularTwoWheelsRobot()
    env.addObject(robot,500,400,-90)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    initialPose=robot.getPose().copy()
    currentState = (robot.getLeftWheel().getSpeed(), robot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState)

    timeLearning = 6
    start=sim.time()

    while True:

        current=sim.time()
        if current-start<timeLearning:
            startPosition=(robot.getPose().getX(),robot.getPose().getY())
            startOrientation = robot.getPose().getOrientation()
            startOrientation %= 360

            # action during 0.1 second to see the result of the action
            action = reinforcementLearning.getActionToExecute()
            robot.setRightWheelSpeed(robot.getRightWheel().getSpeed()+action[0])
            robot.setLeftWheelSpeed(robot.getLeftWheel().getSpeed()+action[1])

            time.sleep(0.1)

            endPosition=(robot.getPose().getX(),robot.getPose().getY())
            endOrientation=robot.getPose().getOrientation()

            distance = sqrt((endPosition[0]-startPosition[0])**2+(endPosition[1]-startPosition[1])**2)

            # reward = distance/(1+(endOrientation-startOrientation)**2) # encourages to go straight
            reward = (endOrientation-startOrientation)/(distance+1) # encourages to turn
            reinforcementLearning.learn(reward)

        else:
            start=sim.time()
            robot.setPose(initialPose.copy())
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
            robot.setCollidedState(False)
            reinforcementLearning.reset()

        time.sleep(.01)


