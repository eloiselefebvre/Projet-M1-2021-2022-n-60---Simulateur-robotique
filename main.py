import time
from Robot import Robot
from Representation import Representation
from Rectangle import Rectangle
from LED import LED
from Wheel import Wheel
from Simulation import Simulation
from Obstacle import Obstacle
from Circle import Circle
from TwoWheelsRobot import TwoWheelsRobot

rob1Rep = Representation(Rectangle(50, 60, "#0490F9", 6))
rob1 = Robot(200, 50, 45, rob1Rep)

led = LED(20, 25, LED.RED)
led2 = LED(20, 40, LED.YELLOW)
led3 = LED(25, 40, LED.GREEN)

wheel = Wheel(0, 10, 10, 8)
wheel2 = Wheel(42, 10, 10, 8)

rob1.addComponent(led)
rob1.addComponent(led2)
rob1.addComponent(wheel)
rob1.addComponent(wheel2)

rob2Rep = Representation(Rectangle(60, 80, "#FFC465", 6))
rob2 = Robot(500, 200, 0, rob2Rep)

wheel3 = Wheel(0, 18, 12, 15)
wheel4 = Wheel(45, 18, 12, 15)

rob2.addComponent(wheel3)
rob2.addComponent(wheel4)
rob2.addComponent(led3)

obs1Rep = Representation(Circle(50,"#FF0"))
obs1 = Obstacle(100,200,0,obs1Rep)

def program():
    ledState = 0
    start=time.time()
    while True:
        if(time.time()-start>1):
            ledState = not ledState
            led.setState(ledState)
            led2.setState(not ledState)
            led3.setState(ledState)
            start=time.time()
        rob1.move(.2,.2)
        rob2.move(0,.3)
        time.sleep(.02)

sim = Simulation()
sim.addObject(rob1)
sim.addObject(rob2)
sim.addObject(obs1)

sim.start(program)


