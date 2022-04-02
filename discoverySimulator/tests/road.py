import time

from discoverySimulator import Object
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Polygon
from discoverySimulator.ressources.maps.CirclePath import CirclePath
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.sensors.ColorSensor import ColorSensor
from discoverySimulator.simulation import Environment, Simulation


def road():

    FORWARD_SPEED=300
    TURN_SPEED=100

    rob1 = RectangularTwoWheelsRobot()
    rob1.enableOdometry()

    colorSensorRight=ColorSensor()
    colorSensorLeft=ColorSensor()

    rob1.addComponent(colorSensorRight,5,25)
    rob1.addComponent(colorSensorLeft,-5,25)

    env=Environment(1200,800)
    polygon=Polygon([(200,500),(300,450),(350,300),(450,250),(550,330),(800,150),(900,160),(950,220),(900,400),(860,430),(780,420),(720,450),
                                           (640,560),(550,610),(400,560),(250,620),(200,580)],"#444")

    env.addVirtualObject(Object(Representation(polygon)))
    polygonOffset = polygon.offset(-30)
    polygonOffset.setColor("#f0f0f0")
    env.addVirtualObject(Object(Representation(polygonOffset)))

    env.addObject(rob1,250,250)


    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    while True:

        if colorSensorRight.getValue()=="#444444" and colorSensorLeft.getValue()=="#444444":
            rob1.setLeftWheelSpeed(FORWARD_SPEED)
            rob1.setRightWheelSpeed(FORWARD_SPEED)
        elif colorSensorRight.getValue()!="#444444" and colorSensorLeft.getValue()=="#444444":
            rob1.setLeftWheelSpeed(-TURN_SPEED)
            rob1.setRightWheelSpeed(TURN_SPEED)
        elif colorSensorRight.getValue()=="#444444" and colorSensorLeft.getValue()!="#444444":
            rob1.setLeftWheelSpeed(TURN_SPEED)
            rob1.setRightWheelSpeed(-TURN_SPEED)
        else:
            rob1.setLeftWheelSpeed(0)
            rob1.setRightWheelSpeed(0)
        sim.sync()