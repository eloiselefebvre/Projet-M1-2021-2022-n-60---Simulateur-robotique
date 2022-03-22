import time

from discoverySimulator.ressources.maps.Maze import Maze
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation

FORWARD_SPEED = 1000
TURN_SPEED = 200
COLLISION_TH = 70

def usingFuzzyLogicToAvoidObstacle():

    rob = RectangularTwoWheelsRobot()

    INFINITY = 10000
    distantObstacle=[]
    rightTurnRightWheel = [0 for _ in range(11)]
    rightTurnLeftWheel = [0 for _ in range(11)]
    leftTurnRightWheel = [0 for _ in range(11)]
    leftTurnLeftWheel = [0 for _ in range(11)]

    for i in range(50):
        distantObstacle.append(0)
    for i in range (50,300):
        distantObstacle.append(i*(5)-250)
    for i in range(300,INFINITY+1):
        distantObstacle.append(100)

    for i in range (-5,6):
        if i<0:
            rightTurnRightWheel[i+5]=(-20*i)
        else:
            rightTurnRightWheel[i+5]=0
        leftTurnLeftWheel[i+5]=rightTurnRightWheel[i+5]
    for i in range (-5,6):
        if i<0:
            rightTurnLeftWheel[i+5]=(20*i)
        else:
            rightTurnRightWheel[i+5]=0
        leftTurnRightWheel[i+5]=rightTurnLeftWheel[i+5]

    leftFrontTelemeter=Telemeter('#dd9999') # left front
    rightFrontTelemeter=Telemeter('#dd9999') # right front
    rightTelemeter=Telemeter('#dd9999')
    leftTelemeter=Telemeter('#dd9999')
    rob.addComponent(leftFrontTelemeter,20,30,-10)
    rob.addComponent(rightFrontTelemeter,-20,30,10)
    rob.addComponent(leftTelemeter, 20, 20, -35)
    rob.addComponent(rightTelemeter, -20, 20, 35)

    env = Environment(4000,2000)
    env.addObject(rob,1000,500,0)

    # env.addObject(Obstacle(Representation(Circle(50,"#ff0"))),800,800)
    # env.addObject(Obstacle(Representation(Circle(50, "#ff0"))), 500, 50)
    # env.addObject(Obstacle(Representation(Circle(50,"#ff0"))),600,600)
    # env.addObject(Obstacle(Representation(Rectangle(200,180,"#0ff"))),800,530)
    # env.addObject(Obstacle(Representation(Circle(90,"#f0f"))),200,250)

    sim = Simulation(env)
    Maze(env)
    sim.run()
    sim.showInterface()

    sim.setAcceleration(5)

    rob.setRightWheelSpeed(FORWARD_SPEED)
    rob.setLeftWheelSpeed(FORWARD_SPEED)

    while True:

        distantObstacleLeftFrontTelemeter = distantObstacle[int(leftFrontTelemeter.getValue())]
        distantObstacleRightFrontTelemeter = distantObstacle[int(rightFrontTelemeter.getValue())]
        distantObstacleRightSensor = distantObstacle[int(rightTelemeter.getValue())]
        distantObstacleLeftSensor = distantObstacle[int(leftTelemeter.getValue())]

        numerator = 0
        denominator = 0

        # roue droite
        for x in range(11):
            cutValueLeftFrontTelemeter = min(distantObstacleLeftFrontTelemeter,rightTurnRightWheel[x])
            cutValueRightFrontTelemeter = min(distantObstacleRightFrontTelemeter,leftTurnRightWheel[x])
            cutValueRightSensor = min(distantObstacleRightSensor,leftTurnRightWheel[x])
            cutValueLeftSensor = min(distantObstacleLeftSensor,rightTurnRightWheel[x])

            numerator += (x-5)*(cutValueLeftFrontTelemeter+cutValueRightFrontTelemeter+cutValueRightSensor+cutValueLeftSensor)
            denominator += (cutValueLeftFrontTelemeter+cutValueRightFrontTelemeter+cutValueRightSensor+cutValueLeftSensor)

        if denominator!=0:
            gravity=numerator/denominator
        else:
            gravity=100
        rob.setRightWheelSpeed(gravity)

        numerator=0
        denominator=0

        # roue gauche
        for x in range (11):
            cutValueLeftFrontTelemeter = min(distantObstacleLeftFrontTelemeter, rightTurnLeftWheel[x])
            cutValueRightFrontTelemeter = min(distantObstacleRightFrontTelemeter, leftTurnLeftWheel[x])
            cutValueRightSensor = min(distantObstacleRightSensor,leftTurnLeftWheel[x])
            cutValueLeftSensor = min(distantObstacleLeftSensor,rightTurnLeftWheel[x])

            numerator += (x-5)*(cutValueLeftFrontTelemeter+cutValueRightFrontTelemeter+cutValueRightSensor+cutValueLeftSensor)
            denominator += (cutValueLeftFrontTelemeter+cutValueRightFrontTelemeter+cutValueRightSensor+cutValueLeftSensor)

        if denominator != 0:
            gravity = numerator / denominator
        else:
            gravity = 100
        rob.setLeftWheelSpeed(gravity)

        time.sleep(.01)
