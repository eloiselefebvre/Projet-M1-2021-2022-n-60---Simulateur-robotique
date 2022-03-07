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
        floors.append(Object(Representation(Rectangle(250,250,"#424949"))))

    for i in range(20):
        obstacles.append(Object(Representation(Rectangle(30,30,"#DC7633"))))

    env = Environment(1525, 1100)
    env.addVirtualObject(floors[0],125,125)
    env.addVirtualObject(floors[1],550,125)
    env.addVirtualObject(floors[2],975,125)
    env.addVirtualObject(floors[3],1400,125)
    env.addVirtualObject(floors[4],125,550)
    env.addVirtualObject(floors[5],550,550)
    env.addVirtualObject(floors[6],975,550)
    env.addVirtualObject(floors[7],1400,550)
    env.addVirtualObject(floors[8],125,975)
    env.addVirtualObject(floors[9],550,975)
    env.addVirtualObject(floors[10],975,975)
    env.addVirtualObject(floors[11],1400,975)

    env.addObject(obstacles[0],40,40)
    env.addObject(obstacles[1],40,120)
    env.addObject(obstacles[2],40,200)
    env.addObject(obstacles[3],120,40)
    env.addObject(obstacles[4],120,120)
    env.addObject(obstacles[5],120,200)
    env.addObject(obstacles[6],200,40)
    env.addObject(obstacles[7],200,120)
    env.addObject(obstacles[8],200,200)
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

