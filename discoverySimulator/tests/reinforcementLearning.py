from discoverySimulator.tools.learning.ReinforcementLearning import ReinforcementLearning
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation

def reinforcementLearningTraining():
    env=Environment(800,800)
    robot=RectangularTwoWheelsRobot()
    env.addObject(robot,50,400,-90)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    initialPose=robot.getPose().copy()
    currentState = (robot.getLeftWheel().getSpeed(), robot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState,[
        {"min":0,"max":600,"intervals":2}, # left wheel
        {"min": 0, "max": 600, "intervals": 2} # right wheel
    ])

    timeLearning = 6
    start=sim.time()

    while sim.time()<10*60:

        current=sim.time()
        if current-start<timeLearning:
            startPosition=(robot.getPose().getX(),robot.getPose().getY())
            startOrientation = robot.getPose().getOrientation()
            startOrientation %= 360

            # action during 0.1 second to see the result of the action
            action = reinforcementLearning.getActionToExecute()
            robot.setRightWheelSpeed(robot.getRightWheel().getSpeed()+action[0])
            robot.setLeftWheelSpeed(robot.getLeftWheel().getSpeed()+action[1])

            sim.sync()

            endPosition=(robot.getPose().getX(),robot.getPose().getY())
            endOrientation=robot.getPose().getOrientation()

            distance = ((endPosition[0]-startPosition[0])**2+(endPosition[1]-startPosition[1])**2)**.5

            reward = distance/(1+(endOrientation-startOrientation)**2) # encourages to go straight
            # reward = (endOrientation-startOrientation)/(distance+1) # encourages to turn
            reinforcementLearning.learn(reward)

        else:
            start=sim.time()
            robot.setPose(initialPose.copy())
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
            robot.setCollidedState(False)
            reinforcementLearning.reset()

        sim.sync()

    reinforcementLearning.saveModel()

def reinforcementLearningFromModel():

    env=Environment(800,800)
    robot=RectangularTwoWheelsRobot()
    env.addObject(robot,50,400,-90)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    currentState = (robot.getLeftWheel().getSpeed(), robot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState)

    reinforcementLearning.loadModel("discoverySimulator/ressources/goForwardTwoWheelsRobotModel.json")

    while True:
        action = reinforcementLearning.getActionToExecute()
        robot.setRightWheelSpeed(robot.getRightWheel().getSpeed()+action[0])
        robot.setLeftWheelSpeed(robot.getLeftWheel().getSpeed()+action[1])
        reinforcementLearning.updateState()
        sim.sync()

