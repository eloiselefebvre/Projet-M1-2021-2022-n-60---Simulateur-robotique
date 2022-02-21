import time

from robotSimulator import Obstacle
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Rectangle, Circle
from robotSimulator.simulation import Environment,Simulation
from robotSimulator.actuators import Buzzer, LED
from robotSimulator.robots import TwoWheelsRobot, FourWheelsRobot
from robotSimulator.sensors import Telemeter

rob1 = TwoWheelsRobot()
rob1.setLeftWheelSpeed(600)
rob1.setRightWheelSpeed(-600)

led = LED(LED.RED)
led2 = LED(LED.YELLOW)
led3 = LED(LED.BLUE)
led4 = LED(LED.YELLOW)

rob1.addComponent(led,0, -10)
rob1.addComponent(led2,0, 10)

rob2 = TwoWheelsRobot()
rob2.addComponent(led3,0, 0)
rob2.setRightWheelSpeed(500)

buzzer = Buzzer()
buzzer2 = Buzzer()
telemeter1 = Telemeter()
telemeter2 = Telemeter()
telemeter3 = Telemeter("#0f0")
telemeter4 = Telemeter("#00f")
rob3 = TwoWheelsRobot("#888",60,80,60)
rob3.addComponent(buzzer,0,0)
rob3.addComponent(buzzer2,0,15)
#rob3.addComponent(telemeter1,-18,30,20)
#rob3.addComponent(telemeter2,18,30,-20)
rob3.addComponent(telemeter3,0,32,0)

rob3.setLeftWheelSpeed(300)
rob3.setRightWheelSpeed(-300)

rob4 = FourWheelsRobot("#f00")
rob4.addComponent(led4,0,0)
rob4.setRightBackWheelSpeed(300)
rob4.setRightFrontWheelSpeed(800)
rob4.setLeftBackWheelSpeed(500)
rob4.setLeftFrontWheelSpeed(-300)

rob5 = TwoWheelsRobot()
rob5.setRightWheelSpeed(300)
rob5.setLeftWheelSpeed(300)

env = Environment()
# env.addObject(rob1,1000, 100, 45)
# env.addObject(rob2,1050, 150, 0)
# env.addObject(rob3,500,500,0)
# env.addObject(rob4,800, 100, 0)
# env.addObject(Obstacle(Representation(Circle(40,"#ff0"))),1000,100)
# env.addObject(Obstacle(Representation(Circle(40,"#f0f"))),1050,100)
env.addObject(rob5,300,250,85)
env.addObject(Obstacle(Representation(Circle(40,"#f0f"))),150,180)
# env.addObject(telemeter4,500,0)
# env.addObject(Telemeter("#ff55f8"),800,0)
# env.addObject(Telemeter("#fa55f8"),0,100,-90)


sim = Simulation(env)
ledState = 0
start=time.time()
sim.setTimeStep(0.0001)

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