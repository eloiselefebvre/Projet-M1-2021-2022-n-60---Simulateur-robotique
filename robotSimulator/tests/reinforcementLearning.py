import random
from math import sqrt

from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.simulation import Simulation, Environment
import time


def reinforcementLearningTest():

    robot = TwoWheelsRobot(100)
    robot.setLeftWheelSpeed(150)
    robot.setRightWheelSpeed(150)

    env = Environment(1500, 1500)
    env.addObject(robot,500,200,-90)
    sim = Simulation(env)

    numberOfColumns = 100
    numberofLines = 100
    envWidth=env.getWidth()
    envHeight=env.getHeight()

    QTable = {}
    startPositionX = int(robot.getPose().getX())
    startPositionY = int(robot.getPose().getY())
    startOrientation = robot.getPose().getOrientation()
    previousStateX=int((startPositionX*numberOfColumns)/envWidth)
    previousStateY=int((startPositionY*numberofLines)/envHeight)
    previousAction=0
    # explorationRate=0.05

    distanceMax=0
    previousDistance=0
    learningFactor=0.1
    for i in range(numberofLines):
        for j in range(numberOfColumns):
            QTable[(i,j)]=[0,0,0]

    sim.run()
    sim.showInterface()
    testTime = 20
    start=sim.time()
    training=1

    while True:

        current=sim.time()
        if current-start<testTime:
            robotCurrentPoseX=robot.getPose().getX()
            robotCurrentPoseY=robot.getPose().getY()
            rightWheelSpeed=robot.getRightWheel().getSpeed()
            currentStateX = int(robotCurrentPoseX*numberOfColumns/envWidth)
            currentStateY = int(robotCurrentPoseY*numberofLines/envHeight)

            if currentStateX!=previousStateX or currentStateY!=previousStateY:
                distance = sqrt((startPositionX - robotCurrentPoseX) ** 2 + (startPositionY - robotCurrentPoseY) ** 2)

                if random.random() < 0 or QTable[(currentStateX, currentStateY)]==[0,0,0]:
                    print("training:", training)
                    previousAction = random.randint(0, 2)
                else:
                    vMax = max(QTable[(previousStateX, previousStateY)])
                    previousAction = QTable[(previousStateX, previousStateY)].index(vMax)

                if previousAction==0:
                    rightWheelSpeed+=50

                elif previousAction==1:
                    rightWheelSpeed-=50

                if distance>distanceMax:
                    distanceMax=distance
                    reward=1
                elif previousDistance<distance:
                    reward=0.5
                else:
                    reward=-2
                QTable[(previousStateX,previousStateY)][previousAction]=(1 - learningFactor) * QTable[(previousStateX, previousStateY)][previousAction] + learningFactor * reward

                previousStateX = currentStateX
                previousStateY = currentStateY
                robot.getRightWheel().setSpeed(rightWheelSpeed)
                previousDistance=distance

        else:
            start=sim.time()
            robot.getPose().move(startPositionX,startPositionY)
            robot.getPose().setOrientation(startOrientation)
            distance=0
            training += 1
            robot.getRightWheel().setSpeed(0)
            previousDistance=0
            robot.setCollidedState(False)

        time.sleep(.01)

# Problème dû au fait que selon l'orientation l'état des actions changent, on doit donc utiliser une position relative et récréer une grille locale selon la position du robot

