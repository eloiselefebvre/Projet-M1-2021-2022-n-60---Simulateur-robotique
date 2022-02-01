import time
from robotSimulator.simulation import Environment,Simulation
from robotSimulator.actuators import Buzzer, LED
from robotSimulator.robots import TwoWheelsRobot, FourWheelsRobot
from robotSimulator.sensors import Telemeter

rob1 = TwoWheelsRobot()
rob1.setLeftWheelSpeed(600)
rob1.setRightWheelSpeed(600)

led = LED(LED.RED)
led2 = LED(LED.YELLOW)
led3 = LED(LED.BLUE)
led4 = LED(LED.YELLOW)

rob1.addComponent(led,0, -10)
rob1.addComponent(led2,0, 10)

rob2 = TwoWheelsRobot()
rob2.addComponent(led3,0, 0)
rob2.setRightWheelSpeed(800)

buzzer = Buzzer()
telemeter1 = Telemeter()
telemeter2 = Telemeter()
telemeter3 = Telemeter("#0f0")
rob3 = TwoWheelsRobot("#888",60,80,60)
rob3.addComponent(buzzer,0,0)
rob3.addComponent(telemeter1,-18,30,20)
rob3.addComponent(telemeter2,18,30,-20)
rob3.addComponent(telemeter3,0,32,0)

rob3.setLeftWheelSpeed(600)
rob3.setRightWheelSpeed(300)

rob4 = FourWheelsRobot("#f00")
rob4.addComponent(led4,0,0)
rob4.setRightBackWheelSpeed(300)
rob4.setRightFrontWheelSpeed(800)
rob4.setLeftBackWheelSpeed(500)
rob4.setLeftFrontWheelSpeed(200)

env = Environment()

env.addObject(rob1,200, 50, 0)
env.addObject(rob2,500, 200, 0)
env.addObject(rob3,500,500,0)
env.addObject(rob4,300, 100, 0)

sim = Simulation(env)

ledState = 0
start=time.time()

sim.run()
sim.showInterface()

i=0
while i<1000:
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