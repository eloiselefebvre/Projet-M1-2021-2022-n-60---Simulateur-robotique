import time
from robotSimulator.simulation import Environment,Simulation
from robotSimulator.actuators import Buzzer, LED
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.sensors import Telemeter

rob1 = TwoWheelsRobot(200, 50, 0)
rob1.setLeftWheelSpeed(0.06)
rob1.setRightWheelSpeed(0.06)

led = LED(0, -10, LED.RED)
led2 = LED(0, 10, LED.YELLOW)
led3 = LED(0, 0, LED.BLUE)

rob1.addComponent(led)
rob1.addComponent(led2)

rob2 = TwoWheelsRobot(500, 200, 0)
rob2.addComponent(led3)
rob2.setRightWheelSpeed(0.08)

buzzer = Buzzer(0,0)
telemeter1 = Telemeter(-18,30,20)
telemeter2 = Telemeter(18,30,-20)
telemeter3 = Telemeter(0,32,0)
rob3 = TwoWheelsRobot(500,500,0,60,80,60)
rob3.addComponent(buzzer)
rob3.addComponent(telemeter1)
rob3.addComponent(telemeter2)
rob3.addComponent(telemeter3)

rob3.setLeftWheelSpeed(0.06)
rob3.setRightWheelSpeed(0.03)

env = Environment()

env.addObject(rob1)
env.addObject(rob2)
env.addObject(rob3)

sim = Simulation(env)

ledState = 0
start=time.time()

sim.showInterface()
i=0
while i<10000:
    if(time.time()-start>1):
        ledState = not ledState
        led.setState(ledState)
        led2.setState(not ledState)
        led3.setState(ledState)
        start=time.time()
    if i==800:
        rob1.setLeftWheelSpeed(0.02)
        rob1.setLeftWheelCCW()
    rob1.move()
    rob2.move()
    rob3.move()
    time.sleep(.02)
    i+=1