import time
from math import sqrt, cos, radians

from discoverySimulator import Pose
from discoverySimulator.ressources.ReinforcementLearning import ReinforcementLearning
from discoverySimulator.robots import TwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation


def reinforcementLearningTest():

    env=Environment(1500,1500)
    robot=TwoWheelsRobot()
    env.addObject(robot,500,400,-90)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    startPosition = (robot.getPose().getX(),robot.getPose().getY())
    startOrientation = robot.getPose().getOrientation()
    if startOrientation<0:
        startOrientation=360+startOrientation
    currentState = (robot.getLeftWheel().getSpeed(), robot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState)
    previousDistance=0
    previousProduit=0
    produitMax=0

    timeLearning = 5
    start=sim.time()

    while True:

        current=sim.time()
        if current-start<timeLearning:
            currentPosition=(robot.getOdometryPose().getX(),robot.getOdometryPose().getY())

            # MSO TODO : il semble y avoir un problème avec la localisation par odométrie : renvoie 90 quand l'orientation réelle est -90
            currentOrientation = robot.getOdometryPose().getOrientation()


            action = reinforcementLearning.getActionToExecute()

            # MSO TODO : à revoir : il faut faire la différence entre deux états successifs, et non avec l'état initial, pour percevoir l'effet de l'action

            distance = sqrt((currentPosition[0]-startPosition[0])**2+(currentPosition[1]-startPosition[1])**2)
            produit = distance * cos(radians(currentOrientation-startOrientation))

            robot.setRightWheelSpeed(robot.getRightWheel().getSpeed()+action[0])
            robot.setLeftWheelSpeed(robot.getLeftWheel().getSpeed()+action[1])

            # MSO : vous pouvez directement utiliser le produit comme récompense
            if produit>produitMax:
                produitMax=produit
                reinforcementLearning.executedActionFeedback(3)
            elif produit < previousProduit :
                reinforcementLearning.executedActionFeedback(1)
            else :
                reinforcementLearning.executedActionFeedback(-1)

            previousProduit=produit
            previousDistance=distance

        else:
            start=sim.time()
            robot.getPose().move(startPosition[0],startPosition[1])
            robot.getPose().setOrientation(startOrientation)
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
            robot.setCollidedState(False)
            previousDistance=0
            previousProduit=0
            robot.setOdometryPose(Pose(startPosition[0],startPosition[1],startOrientation))
            reinforcementLearning.reset()

        time.sleep(.01)


