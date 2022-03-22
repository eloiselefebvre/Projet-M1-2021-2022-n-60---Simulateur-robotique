import time

from discoverySimulator import Obstacle, Object
from discoverySimulator.actuators import LED, Buzzer
from discoverySimulator.obstacles.CircularObstacle import CircularObstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle, Line, Polygon
from discoverySimulator.robots import RectangularTwoWheelsRobot, FourWheelsRobot, CircularTwoWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.sensors.ColorSensor import ColorSensor
from discoverySimulator.simulation import Environment, Simulation


def collisionAndTelemeter():

    rob1 = RectangularTwoWheelsRobot()
    colorSensorRight=ColorSensor()
    rob1.addComponent(colorSensorRight,5,25)
    colorSensorLeft=ColorSensor()
    rob1.addComponent(colorSensorLeft,-5,25)
    rob1.setRightWheelSpeed(200)
    rob1.setLeftWheelSpeed(200)
    # rob1.setID("2W")

    led = LED(LED.RED)
    led2 = LED(LED.YELLOW)
    led3 = LED(LED.BLUE)
    led4 = LED(LED.YELLOW)

    rob1.addComponent(led, 0, -10)
    rob1.addComponent(led2, 0, 10)


    rob2 = CircularTwoWheelsRobot()
    rob2.addComponent(led3, 0, 0)
    rob2.setRightWheelSpeed(200)
    rob2.setLeftWheelSpeed(300)
    # rob2.setID("2W")

    colorSensor = ColorSensor("#999999")
    rob2.addComponent(colorSensor,0,0,0)

    buzzer = Buzzer()
    telemeter = Telemeter("#0f0")
    telemeter.setID("Front Telemeter")
    rob3 = RectangularTwoWheelsRobot("#F97F51", 60, 80, 60)
    rob3.addComponent(buzzer, 0, 0)
    rob3.addComponent(telemeter, 0, 32, 0)

    rob3.setLeftWheelSpeed(200)
    rob3.setRightWheelSpeed(100)

    rob4 = FourWheelsRobot("#f00")
    rob4.addComponent(led4, 0, 0)
    rob4.setRightBackWheelSpeed(300)
    rob4.setRightFrontWheelSpeed(300)
    rob4.setLeftBackWheelSpeed(500)
    rob4.setLeftFrontWheelSpeed(-300)

    rob5 = RectangularTwoWheelsRobot()
    rob5.setRightWheelSpeed(300)
    rob5.setLeftWheelSpeed(300)

    # polygon=Object(Representation(Polygon([(300,200),(400,200),(500,300),(400,350),(350,300)],"#f0f")))

    env = Environment(1500,900)
    env.addObject(rob1, 1000, 100, 30)
    env.addObject(rob2, 1050, 300, 0)
    env.addObject(rob3, 500, 500, 45)
    env.addObject(rob4, 700, 500, 90)
    env.addObject(rob5, 700, 180, 90)
    env.addObject(CircularObstacle(40, "#ff8fff"), 150, 180)
    env.addObject(Telemeter(),500,4)
    # env.addObject(polygon,100,100)
    env.addVirtualObject(CircularObstacle(50,'#ff8f8f'),600,600)

    sim = Simulation(env)
    ledState = 0
    start = sim.time()
    # sim.setAcceleration(2)
    sim.run()
    sim.showInterface()

    while True:
        current = sim.time()
        if current-start>1:
            start=current
            ledState=not ledState
            led.setState(ledState)
            led2.setState(not ledState)
            led3.setState(ledState)
            led4.setState(ledState)

        time.sleep(.01)
