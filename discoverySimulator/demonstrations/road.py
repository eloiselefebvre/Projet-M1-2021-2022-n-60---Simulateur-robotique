import time
from discoverySimulator import Object
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Line, Circle, Rectangle
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.sensors.ColorSensor import ColorSensor
from discoverySimulator.simulation import Environment, Simulation


def roadDemo():

    FORWARD_SPEED = 300
    TURN_SPEED = 100

    envWidth=1500
    envHeight=1000
    color="#5f6b6d"
    red="#ff0033"
    green="#33ff00"

    robot = RectangularTwoWheelsRobot()
    colorSensorRight = ColorSensor()
    robot.addComponent(colorSensorRight, 5, 25)
    colorSensorLeft = ColorSensor()
    robot.addComponent(colorSensorLeft, -5, 25)


    start=Object(Representation(Rectangle(20,5,green)))
    finish=Object(Representation(Rectangle(20,5,red)))
    radius1=200
    radius2=300

    env = Environment(envWidth, envHeight)
    env.addObject(robot, 380, 400)

    circle1 = Object(Representation(Circle(radius1,color)))
    circle2 = Object(Representation(Circle(radius1 - 20, "#f0f0f0")))
    circle3 = Object(Representation(Circle(radius2,color)))
    circle4 = Object(Representation(Circle(radius2 - 20, "#f0f0f0")))
    env.addVirtualObject(circle1, int(envWidth/ 2) - radius1,int(envHeight/ 2))
    env.addVirtualObject(circle2, int(envWidth/ 2) - radius1,int(envHeight/ 2))
    env.addVirtualObject(circle3, int(envWidth/ 2) - 20 + radius2,int(envHeight/ 2))
    env.addVirtualObject(circle4, int(envWidth/ 2) - 20 + radius2,int(envHeight/ 2))
    env.addVirtualObject(start,int(envWidth/2)-2*radius1+10,int(envHeight/ 2))
    env.addVirtualObject(finish,int(envWidth/2)+2*radius2-30,int(envHeight/ 2))

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    while True:

        if colorSensorRight.getValue() == green or colorSensorLeft.getValue() == green :
            # print("START !")
            FORWARD_SPEED+=50
            TURN_SPEED+=50
            robot.setRightWheelSpeed(FORWARD_SPEED)
            robot.setLeftWheelSpeed(FORWARD_SPEED)
        elif colorSensorRight.getValue() == color and colorSensorLeft.getValue() == color:
            robot.setLeftWheelSpeed(FORWARD_SPEED)
            robot.setRightWheelSpeed(FORWARD_SPEED)
        elif colorSensorRight.getValue() != color and colorSensorLeft.getValue() == color:
            robot.setLeftWheelSpeed(-TURN_SPEED)
            robot.setRightWheelSpeed(TURN_SPEED)
        elif colorSensorRight.getValue() == color and colorSensorLeft.getValue() != color:
            robot.setRightWheelSpeed(-TURN_SPEED)
            robot.setLeftWheelSpeed(TURN_SPEED)
        elif colorSensorRight.getValue() == red or colorSensorLeft.getValue() == red:
            # print("FINISHED !")
            robot.setRightWheelSpeed(0)
            robot.setLeftWheelSpeed(0)
        else:
            # print("Out of path !")
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
        print("ok")
        sim.sync()