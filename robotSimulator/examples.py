# MSO TODO : faire un package "examples" avec les exemples que l'on va vraiment laisser aux étudiants pour illustration
# mettre un exemple de navigation simple avec le télémètre (du genre : si obstacle détecté à gauche tourner à droite) --> ce que pourraient coder des débutants avec des ifs sur des seuils

# MSO TODO : faire un autre package "tests" avec vos tests, comme celui-ci. Il est intéressant de les garder, au moins pendant la durée du projet - mais l'objectif est différent

import time

from robotSimulator import Obstacle
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Rectangle, Circle
from robotSimulator.ressources.maps.Maze import Maze
from robotSimulator.simulation import Environment,Simulation
from robotSimulator.actuators import Buzzer, LED
from robotSimulator.robots import TwoWheelsRobot, FourWheelsRobot
from robotSimulator.sensors import Telemeter, LIDAR

FORWARD_SPEED = 1000
TURN_SPEED = 200
COLLISION_TH = 70

def collisionAndTelemeter():
    rob1 = TwoWheelsRobot()
    rob1.setLeftWheelSpeed(600)
    rob1.setRightWheelSpeed(-600)
    # rob1.setID("2W")

    led = LED(LED.RED)
    led2 = LED(LED.YELLOW)
    led3 = LED(LED.BLUE)
    led4 = LED(LED.YELLOW)

    rob1.addComponent(led, 0, -10)
    rob1.addComponent(led2, 0, 10)

    rob2 = TwoWheelsRobot()
    rob2.addComponent(led3, 0, 0)
    rob2.setRightWheelSpeed(500)
    # rob2.setID("2W")

    buzzer = Buzzer()
    telemeter = Telemeter("#0f0")
    # telemeter.setID("Front Telemeter")
    rob3 = TwoWheelsRobot("#F97F51", 60, 80, 60)
    rob3.addComponent(buzzer, 0, 0)
    rob3.addComponent(telemeter, 0, 32, 0)

    rob3.setLeftWheelSpeed(300)
    rob3.setRightWheelSpeed(-300)

    rob4 = FourWheelsRobot("#f00")
    rob4.addComponent(led4, 0, 0)
    rob4.setRightBackWheelSpeed(300)
    rob4.setRightFrontWheelSpeed(800)
    rob4.setLeftBackWheelSpeed(500)
    rob4.setLeftFrontWheelSpeed(-300)

    rob5 = TwoWheelsRobot()
    rob5.setRightWheelSpeed(300)
    rob5.setLeftWheelSpeed(300)

    env = Environment(1500,900)
    env.addObject(rob1, 1000, 100, 45)
    env.addObject(rob2, 1050, 150, 0)
    env.addObject(rob3, 500, 500, 90)
    env.addObject(rob4, 700, 500, 90)
    env.addObject(rob5, 300, 180, 90)
    env.addObject(Obstacle(Representation(Circle(40, "#ff8fff"))), 150, 180)

    sim = Simulation(env)
    ledState = 0
    start = sim.time()
    sim.setAcceleration(2)
    sim.run()
    sim.showInterface()

    while True:
        current = sim.time()
        if current - start > 1:
            ledState = not ledState
            led.setState(ledState)
            led2.setState(not ledState)
            led3.setState(ledState)
            led4.setState(ledState)
            start = current
        time.sleep(.01)



def simpleAvoidingObstacle():
    rob = TwoWheelsRobot("#888",60,80,60)

    telemeters = []

    o=25
    x=-20
    y=20

    for i in range(6):
        telemeters.append(Telemeter())
        rob.addComponent(telemeters[-1],x,y,o)
        o-=10
        x+=8
        if i<2:
            y+=5
        elif  i>2:
            y-=5

    env = Environment(1500,900)
    env.addObject(rob,500,500,90)

    #env.addObject(Obstacle(Representation(Circle(40,"#f0f"))),0,300)
    env.addObject(Obstacle(Representation(Circle(50,"#ff0"))),800,800)
    env.addObject(Obstacle(Representation(Rectangle(200,180,"#0ff"))),750,530)
    env.addObject(Obstacle(Representation(Circle(90,"#f0f"))),1000,300)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    sim.setAcceleration(100)

    while True:
        # for i in range(6):
        #     print(i,":",telemeters[i].getValue())

        if (telemeters[0].getValue()<COLLISION_TH) or (telemeters[1].getValue()<COLLISION_TH) or (telemeters[2].getValue()<COLLISION_TH) and (telemeters[3].getValue()<COLLISION_TH) or (telemeters[4].getValue()<COLLISION_TH) or (telemeters[5].getValue()<COLLISION_TH):
            rob.setLeftWheelSpeed(TURN_SPEED)
            rob.setRightWheelSpeed(-TURN_SPEED)

        elif (telemeters[0].getValue()<COLLISION_TH) or (telemeters[1].getValue()<COLLISION_TH) or (telemeters[2].getValue()<COLLISION_TH):
            rob.setLeftWheelSpeed(-TURN_SPEED)
            rob.setRightWheelSpeed(TURN_SPEED)

        elif (telemeters[3].getValue()<COLLISION_TH) or (telemeters[4].getValue()<COLLISION_TH) or (telemeters[5].getValue()<COLLISION_TH):
            rob.setLeftWheelSpeed(TURN_SPEED)
            rob.setRightWheelSpeed(-TURN_SPEED)

        else:
            rob.setLeftWheelSpeed(FORWARD_SPEED)
            rob.setRightWheelSpeed(FORWARD_SPEED)
        time.sleep(.01)

def usingFuzzyLogicToAvoidObstacle():

    rob = TwoWheelsRobot()

    INFINITY = 100000  # MSO TODO : utiliser float("inf")
    distantObstacle=[]
    rightTurnRightWheel = [0 for _ in range(11)]
    rightTurnLeftWheel = [0 for _ in range(11)]
    leftTurnRightWheel = [0 for _ in range(11)]
    leftTurnLeftWheel = [0 for _ in range(11)]

    for i in range(50):
        distantObstacle.append(0)
    for i in range (50,300):
        distantObstacle.append(i*(5)-250)
    for i in range(300,INFINITY):
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
    env.addObject(rob,1000,500,100)
    # map = Map(env)
    # map.generateObstacles()

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


def LIDARTest():
    lidar = LIDAR()
    rob = TwoWheelsRobot()
    rob.addComponent(lidar)
    rob.setRightWheelSpeed(400)
    rob.setLeftWheelSpeed(400)

    lidar2 = LIDAR("#00f")
    rob2 = TwoWheelsRobot()
    rob2.addComponent(lidar2)
    rob2.setRightWheelSpeed(200)
    rob2.setLeftWheelSpeed(400)

    env = Environment(1500,900)
    env.addObject(rob, 500, 500)
    env.addObject(rob2, 900, 500)
    env.addObject(Obstacle(Representation(Circle(40, "#ff8fff"))), 150, 180)
    env.addObject(Obstacle(Representation(Rectangle(40,200, "#ff8fff"))), 650, 400)
    env.addObject(Obstacle(Representation(Rectangle(400, 100, "#ff8fff"))), 250, 850,25)

    sim = Simulation(env)
    sim.setAcceleration(1)
    sim.run()
    sim.showInterface()