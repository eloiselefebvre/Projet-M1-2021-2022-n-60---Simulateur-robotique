import time

from discoverySimulator import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle, Rectangle
from discoverySimulator.robots import TwoWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation

FORWARD_SPEED = 1000
TURN_SPEED = 200
COLLISION_TH = 70

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

