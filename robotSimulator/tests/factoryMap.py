from robotSimulator import Obstacle, Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Rectangle
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.sensors.ColorSensor import ColorSensor
from robotSimulator.simulation import Environment, Simulation
import time

def factoryMap():

    FORWARD_SPEED=300
    TURN_SPEED=100

    rob1 = TwoWheelsRobot()
    colorSensorRight=ColorSensor()
    rob1.addComponent(colorSensorRight,20,25)
    colorSensorLeft=ColorSensor()
    rob1.addComponent(colorSensorLeft,-20,25)

    obstacles=[]
    floors=[]


    for i in range(12):
        floors.append(Object(Representation(Rectangle(250,250,"#444"))))

    for i in range(20):
        obstacles.append(Object(Representation(Rectangle(30,30,"#DC7633"))))

    env = Environment(1525, 1100)
    i=0

    while i<=11:
        for y in range (125,976,425):
            for x in range (125,1401,425):
                env.addVirtualObject(floors[i],x,y)
                i+=1

    j=0
    while j<=9:
        for y in range(40,201,80):
            for x in range(40,201,80):
                env.addObject(obstacles[j],x,y)
                j+=1

    env.addObject(rob1,230,300,-60)

    sim = Simulation(env)

    sim.run()
    sim.showInterface()


    while True:
        if  colorSensorRight.getValue()!="#f0f0f0" and colorSensorLeft.getValue()!="#f0f0f0":
            rob1.setLeftWheelSpeed(-FORWARD_SPEED/2)
            rob1.setRightWheelSpeed(-FORWARD_SPEED)
        elif colorSensorRight.getValue()!="#f0f0f0":
            rob1.setLeftWheelSpeed(TURN_SPEED)
            rob1.setRightWheelSpeed(-FORWARD_SPEED/2)
        elif colorSensorLeft.getValue()!="#f0f0f0":
            rob1.setRightWheelSpeed(TURN_SPEED)
            rob1.setLeftWheelSpeed(-FORWARD_SPEED/2)
        else:
            rob1.setRightWheelSpeed(FORWARD_SPEED)
            rob1.setLeftWheelSpeed(FORWARD_SPEED)
        time.sleep(.01)

