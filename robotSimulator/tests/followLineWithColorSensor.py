import time

from robotSimulator.ressources.maps.Path import Path
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

    env=Environment(1500,1500)
    env.addObject(rob1,250,250)

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
            # print("Out of path !")
            rob1.setLeftWheelSpeed(0)
            rob1.setRightWheelSpeed(0)

        time.sleep(.01)

