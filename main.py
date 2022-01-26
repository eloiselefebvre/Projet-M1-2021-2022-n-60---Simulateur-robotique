import time
from robotSimulator.simulation import Environment,Simulation
from robotSimulator.actuators import Buzzer, LED
from robotSimulator.robots import TwoWheelsRobot, FourWheelsRobot
from robotSimulator.sensors import Telemeter

rob1 = TwoWheelsRobot(200, 50, 0)
rob1.setLeftWheelSpeed(600)
rob1.setRightWheelSpeed(600)

led = LED(0, -10, LED.RED)
led2 = LED(0, 10, LED.YELLOW)
led3 = LED(0, 0, LED.BLUE)
led4 = LED(0,0,LED.YELLOW)

rob1.addComponent(led)
rob1.addComponent(led2)

rob2 = TwoWheelsRobot(500, 200, 0)
rob2.addComponent(led3)
rob2.setRightWheelSpeed(800)

buzzer = Buzzer(0,0)
telemeter1 = Telemeter(-18,30,20)
telemeter2 = Telemeter(18,30,-20)
telemeter3 = Telemeter(0,32,0)
rob3 = TwoWheelsRobot(500,500,0,60,80,60)
rob3.addComponent(buzzer)
rob3.addComponent(telemeter1)
rob3.addComponent(telemeter2)
rob3.addComponent(telemeter3)

rob3.setLeftWheelSpeed(600)
rob3.setRightWheelSpeed(300)

rob4 = FourWheelsRobot(300, 100, 0)
rob4.addComponent(led4)
rob4.setRightBackWheelSpeed(300)
rob4.setRightFrontWheelSpeed(800)
rob4.setLeftBackWheelSpeed(500)
rob4.setLeftFrontWheelSpeed(200)

env = Environment()

env.addObject(rob1)
env.addObject(rob2)
env.addObject(rob3)
env.addObject(rob4)

sim = Simulation(env)

ledState = 0
start=time.time()

sim.run()
sim.showInterface()
i=0
while i<10000:
    current = time.time()
    if current-start>1:
        ledState = not ledState
        led.setState(ledState)
        led2.setState(not ledState)
        led3.setState(ledState)
        led4.setState(ledState)
        start=current
    time.sleep(.01)
    i+=1