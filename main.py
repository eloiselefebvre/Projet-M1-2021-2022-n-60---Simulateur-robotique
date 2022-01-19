import time
from robotSimulator.Environment import Environment
from robotSimulator.actuators.Buzzer import Buzzer
from robotSimulator.robots.Robot import Robot
from robotSimulator.robots.TwoWheelsRobot import TwoWheelsRobot
from robotSimulator.Representation import Representation
from robotSimulator.Rectangle import Rectangle
from robotSimulator.actuators.LED import LED
from robotSimulator.actuators.Wheel import Wheel
from robotSimulator.Simulation import Simulation
from robotSimulator.sensors.Telemeter import Telemeter

rob1Rep = Representation(Rectangle(50, 60, "#0490F9", 6))

rob1 = Robot(200, 50, 45, rob1Rep)

led = LED(0, -10, LED.RED)
led2 = LED(0, 10, LED.YELLOW)
led3 = LED(0, 0, LED.GREEN)

wheel = Wheel(-21, 0, 10, 8)
wheel2 = Wheel(21, 0, 10, 8)

rob1.addComponent(led)
rob1.addComponent(led2)
rob1.addComponent(wheel)
rob1.addComponent(wheel2)

rob2Rep = Representation(Rectangle(60, 80, "#FFC465", 6))

rob2 = Robot(500, 200, 0, rob2Rep)

wheel3 = Wheel(-22, 0, 12, 15)
wheel4 = Wheel(22, 0, 12, 15)

rob2.addComponent(wheel3)
rob2.addComponent(wheel4)
rob2.addComponent(led3)


buzzer = Buzzer(0,0)
telemeter = Telemeter(0,15,20)
rob3 = TwoWheelsRobot(500,500,0)
rob3.addComponent(buzzer)
rob3.addComponent(telemeter)

rob3.setLeftWheelSpeed(0.004)
rob3.setRightWheelSpeed(-0.006)

env = Environment()

env.addObject(rob1)
env.addObject(rob2)

env.addObject(rob3)

sim = Simulation(env)

ledState = 0
start=time.time()

sim.show()
i=0
while i<1000:
    if(time.time()-start>1):
        ledState = not ledState
        led.setState(ledState)
        led2.setState(not ledState)
        led3.setState(ledState)
        start=time.time()

    rob3.move()
    time.sleep(.02)
    i+=1