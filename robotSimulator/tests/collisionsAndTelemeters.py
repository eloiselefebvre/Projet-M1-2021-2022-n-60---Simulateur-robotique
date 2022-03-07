import time

from robotSimulator import Obstacle
from robotSimulator.actuators import LED, Buzzer
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Circle
from robotSimulator.robots import TwoWheelsRobot, FourWheelsRobot
from robotSimulator.sensors import Telemeter
from robotSimulator.sensors.ColorSensor import ColorSensor
from robotSimulator.simulation import Environment, Simulation


def collisionAndTelemeter():
    rob1 = TwoWheelsRobot()
    rob1.setLeftWheelSpeed(600)
    rob1.setRightWheelSpeed(-600)
    # rob1.setID("2W")

    led = LED(LED.RED)
    led2 = LED(LED.YELLOW)
    led3 = LED(LED.BLUE)
    led4 = LED(LED.YELLOW)

    # rob1.addComponent(led, 0, -10)
    # rob1.addComponent(led2, 0, 10)


    rob2 = TwoWheelsRobot()
    rob2.addComponent(led3, 0, 0)
    rob2.setRightWheelSpeed(500)
    rob2.setLeftWheelSpeed(300)
    # rob2.setID("2W")

    colorSensor = ColorSensor("#999999")
    rob2.addComponent(colorSensor,0,0,0)

    buzzer = Buzzer()
    telemeter = Telemeter("#0f0")
    # telemeter.setID("Front Telemeter")
    rob3 = TwoWheelsRobot("#F97F51", 60, 80, 60)
    rob3.addComponent(buzzer, 0, 0)
    rob3.addComponent(telemeter, 0, 32, 0)

    rob3.setLeftWheelSpeed(400)
    rob3.setRightWheelSpeed(200)

    rob4 = FourWheelsRobot("#f00")
    rob4.addComponent(led4, 0, 0)
    rob4.setRightBackWheelSpeed(300)
    rob4.setRightFrontWheelSpeed(300)
    rob4.setLeftBackWheelSpeed(500)
    rob4.setLeftFrontWheelSpeed(-300)

    rob5 = TwoWheelsRobot()
    rob5.setRightWheelSpeed(300)
    rob5.setLeftWheelSpeed(300)

    env = Environment(1500,900)
    # env.addObject(rob1, 1000, 100, 45)
    env.addObject(rob2, 1050, 300, 0)
    # env.addObject(rob3, 500, 500, 90)
    # env.addObject(rob4, 700, 500, 90)
    # env.addObject(rob5, 700, 180, 90)
    # env.addObject(Obstacle(Representation(Circle(40, "#ff8fff"))), 150, 180)
    # env.addVirtualObject(Obstacle(Representation(Circle(200,'#ff8f8f'))),1000,500)

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
