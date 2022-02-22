import time

from robotSimulator import Obstacle
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Rectangle, Circle
from robotSimulator.simulation import Environment,Simulation
from robotSimulator.actuators import Buzzer, LED
from robotSimulator.robots import TwoWheelsRobot, FourWheelsRobot
from robotSimulator.sensors import Telemeter

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

    env = Environment()
    env.addObject(rob,500,500,90)

    #env.addObject(Obstacle(Representation(Circle(40,"#f0f"))),0,300)
    env.addObject(Obstacle(Representation(Circle(50,"#ff0"))),800,800)
    env.addObject(Obstacle(Representation(Rectangle(200,180,"#0ff"))),1200,600)
    env.addObject(Obstacle(Representation(Circle(90,"#f0f"))),1000,20)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    sim.setAcceleration(50)

    FORWARD_SPEED = 1000
    TURN_SPEED = 200
    COLLISION_TH = 70

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

def collisionAndTelemeter():
    rob1 = TwoWheelsRobot()
    rob1.setLeftWheelSpeed(600)
    rob1.setRightWheelSpeed(-600)

    led = LED(LED.RED)
    led2 = LED(LED.YELLOW)
    led3 = LED(LED.BLUE)
    led4 = LED(LED.YELLOW)

    rob1.addComponent(led, 0, -10)
    rob1.addComponent(led2, 0, 10)

    rob2 = TwoWheelsRobot()
    rob2.addComponent(led3, 0, 0)
    rob2.setRightWheelSpeed(500)

    buzzer = Buzzer()
    telemeter = Telemeter("#0f0")
    rob3 = TwoWheelsRobot("#888", 60, 80, 60)
    rob3.addComponent(buzzer, 0, 0)
    rob3.addComponent(telemeter, 0, 32, 0)

    rob3.setLeftWheelSpeed(300)
    rob3.setRightWheelSpeed(-300)

    rob4 = FourWheelsRobot("#f00")
    rob4.addComponent(led4, 0, 0)
    rob4.setRightBackWheelSpeed(300)
    rob4.setRightFrontWheelSpeed(800)
    rob4.setLeftBackWheelSpeed(500)
    rob4.setLeftFrontWheelSpeed(-300)

    rob5 = TwoWheelsRobot()
    rob5.setRightWheelSpeed(300)
    rob5.setLeftWheelSpeed(300)

    env = Environment()
    env.addObject(rob1, 1000, 100, 45)
    env.addObject(rob2, 1050, 150, 0)
    env.addObject(rob3, 500, 500, 90)
    env.addObject(rob5, 300, 180, 90)
    env.addObject(Obstacle(Representation(Circle(40, "#ff8fff"))), 150, 180)

    sim = Simulation(env)
    ledState = 0
    start = time.time()
    sim.setAcceleration(1)
    sim.run()
    sim.showInterface()

    while True:
        current = time.time()
        if current - start > 1:
            ledState = not ledState
            led.setState(ledState)
            led2.setState(not ledState)
            led3.setState(ledState)
            led4.setState(ledState)
            start = current
        time.sleep(.01)
