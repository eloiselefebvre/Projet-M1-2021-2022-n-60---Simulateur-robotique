import time

from robotSimulator import Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Rectangle, Circle
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.sensors.ColorSensor import ColorSensor
from robotSimulator.simulation import Environment, Simulation


def followLineWithColorSensor():

    FORWARD_SPEED=300
    TURN_SPEED=100

    rob1 = TwoWheelsRobot()
    colorSensorRight=ColorSensor()
    rob1.addComponent(colorSensorRight,5,25)
    colorSensorLeft=ColorSensor()
    rob1.addComponent(colorSensorLeft,-5,25)
    rob1.setRightWheelSpeed(200)
    rob1.setLeftWheelSpeed(200)

    obs1=Object(Representation(Rectangle(980,20,"#444")))
    obs2=Object(Representation(Rectangle(980,20,"#444")))
    obs3=Object(Representation(Rectangle(980,20,"#444")))
    obs4=Object(Representation(Rectangle(980,20,"#444")))
    c1=Object(Representation(Circle(20,"#444")))
    c2=Object(Representation(Circle(20,"#444")))
    c3=Object(Representation(Circle(20,"#444")))
    c4=Object(Representation(Circle(20,"#444")))
    c5=Object(Representation(Circle(20,"#f0f0f0")))
    c6=Object(Representation(Circle(20,"#f0f0f0")))
    c7=Object(Representation(Circle(20,"#f0f0f0")))
    c8=Object(Representation(Circle(20,"#f0f0f0")))


    envWidth=1500
    envHeight=1500
    env=Environment(envWidth,envHeight)
    env.addObject(rob1,250,250)
    env.addVirtualObject(obs1,envWidth-250,envHeight/2,-90)
    env.addVirtualObject(obs2,envWidth/2,envHeight-250)
    env.addVirtualObject(obs3,250,envHeight/2,-90)
    env.addVirtualObject(obs4,envWidth/2,250)
    env.addVirtualObject(c1,250+10,250+10)
    env.addVirtualObject(c2,250+10,envHeight-250-10)
    env.addVirtualObject(c3,envWidth-250-10,250+10)
    env.addVirtualObject(c4,envHeight-250-10,envWidth-250-10)
    env.addVirtualObject(c5, 250 + 30, 250 + 30)
    env.addVirtualObject(c6, 250 + 30, envHeight - 250 - 30)
    env.addVirtualObject(c7, envWidth - 250 - 30, 250 + 30)
    env.addVirtualObject(c8, envHeight - 250 - 30, envWidth - 250 - 30)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    while True:

        if colorSensorRight.getValue()=="#444444" and colorSensorLeft.getValue()=="#444444":
            rob1.setLeftWheelSpeed(FORWARD_SPEED)
            rob1.setRightWheelSpeed(FORWARD_SPEED)
        elif colorSensorRight.getValue()!="#444444" and colorSensorLeft.getValue()=="#444444":
            rob1.setLeftWheelSpeed(TURN_SPEED)
            rob1.setRightWheelSpeed(-TURN_SPEED)
        elif colorSensorRight.getValue()=="#444444" and colorSensorLeft.getValue()!="#444444":
            rob1.setRightWheelSpeed(TURN_SPEED)
            rob1.setLeftWheelSpeed(-TURN_SPEED)
        else:
            rob1.setLeftWheelSpeed(0)
            rob1.setRightWheelSpeed(0)

        time.sleep(.01)

