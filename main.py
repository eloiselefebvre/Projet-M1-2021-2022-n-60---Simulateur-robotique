import time
from robotSimulator.Environment import Environment
from robotSimulator.robots.Robot import Robot
from robotSimulator.robots.TwoWheelsRobot import TwoWheelsRobot
from robotSimulator.Representation import Representation
from robotSimulator.Rectangle import Rectangle
from robotSimulator.actuators.LED import LED
from robotSimulator.actuators.Wheel import Wheel
from robotSimulator.Simulation import Simulation

rob1Rep = Representation(Rectangle(50, 60, "#0490F9", 6))

rob1 = Robot(200, 50, 45, rob1Rep)

led = LED(0, -10, LED.RED)
led2 = LED(0, 10, LED.YELLOW)
led3 = LED(0, 0, LED.GREEN)

wheel = Wheel(-21, 10, 10, 8)
wheel2 = Wheel(21, 10, 10, 8)

rob1.addComponent(led)
rob1.addComponent(led2)
rob1.addComponent(wheel)
rob1.addComponent(wheel2)

rob2Rep = Representation(Rectangle(60, 80, "#FFC465", 6))

rob2 = Robot(500, 200, 0, rob2Rep)

wheel3 = Wheel(-22, 10, 12, 15)
wheel4 = Wheel(22, 10, 12, 15)

rob2.addComponent(wheel3)
rob2.addComponent(wheel4)
rob2.addComponent(led3)

rob3 = TwoWheelsRobot(500,500,0)
rob3.addComponent(led2)

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
    rob1.move(.2,.2)
    rob2.move(0,.3)
    rob3.move(0.4, .3)
    time.sleep(.02)
    i+=1