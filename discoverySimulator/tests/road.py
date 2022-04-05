from discoverySimulator import Object
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle, Rectangle
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.sensors.ColorSensor import ColorSensor
from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.representation.shapes import Polygon


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
        sim.sync()

def road():
    rob1 = RectangularTwoWheelsRobot()
    rob1.enableOdometry()
    FORWARD_SPEED = 300
    TURN_SPEED = 100

    colorSensorRight = ColorSensor()
    colorSensorLeft = ColorSensor()


    rob1.addComponent(colorSensorRight, 5, 25)
    rob1.addComponent(colorSensorLeft, -5, 25)

    env = Environment(1200, 800)
    polygon = Polygon(
        [(200, 500), (300, 450), (350, 300), (450, 250), (550, 330), (800, 150), (900, 160), (950, 220), (900, 400),
         (860, 430), (780, 420), (720, 450),
         (640, 560), (550, 610), (400, 560), (250, 620), (200, 580)], "#444")

    env.addVirtualObject(Object(Representation(polygon)))
    polygonOffset = polygon.offset(-30)
    polygonOffset.setColor("#f0f0f0")
    env.addVirtualObject(Object(Representation(polygonOffset)))

    env.addObject(rob1, 250, 250)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    while True:
        if colorSensorRight.getValue() == "#444444" and colorSensorLeft.getValue() == "#444444":
            rob1.setLeftWheelSpeed(FORWARD_SPEED)
            rob1.setRightWheelSpeed(FORWARD_SPEED)
        elif colorSensorRight.getValue() != "#444444" and colorSensorLeft.getValue() == "#444444":
            rob1.setLeftWheelSpeed(-TURN_SPEED)
            rob1.setRightWheelSpeed(TURN_SPEED)
        elif colorSensorRight.getValue() == "#444444" and colorSensorLeft.getValue() != "#444444":
            rob1.setLeftWheelSpeed(TURN_SPEED)
            rob1.setRightWheelSpeed(-TURN_SPEED)
        else:
            rob1.setLeftWheelSpeed(0)
            rob1.setRightWheelSpeed(0)
        sim.sync()