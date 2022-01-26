import time
from robotSimulator.simulation import Environment,Simulation
from robotSimulator.actuators import Buzzer, LED
from robotSimulator.robots import TwoWheelsRobot, FourWheelsRobot
from robotSimulator.sensors import Telemeter

rob1 = TwoWheelsRobot(200, 50, 0)
rob1.setLeftWheelSpeed(0.06)
rob1.setRightWheelSpeed(0.06)

led = LED(0, -10, LED.RED)      # MSO : TODO : Retirer les coordonnées d'installation
led2 = LED(0, 10, LED.YELLOW)
led3 = LED(0, 0, LED.BLUE)
led4 = LED(0,0,LED.YELLOW)

rob1.addComponent(led)      # MSO : TODO : les coordonnées d'installation devraient se trouver dans addComponent, et non dans les contructeurs des composants.
rob1.addComponent(led2)     # Ex : je crée une LED rouge, puis je l'installe en (10, 0) sur le robot. Cette position n'a de sens qu'au moment de l'installation, elle est relative au robot, que l'on ne connait pas au moment d'instancier le composant

rob2 = TwoWheelsRobot(500, 200, 0)
rob2.addComponent(led3)
rob2.setRightWheelSpeed(0.08)

buzzer = Buzzer(0,0)
telemeter1 = Telemeter(-18,30,20)   # MSO : Retirer les coordonnées d'installation
telemeter2 = Telemeter(18,30,-20)
telemeter3 = Telemeter(0,32,0)
rob3 = TwoWheelsRobot(500,500,0,60,80,60)
rob3.addComponent(buzzer)
rob3.addComponent(telemeter1)
rob3.addComponent(telemeter2)
rob3.addComponent(telemeter3)

rob3.setLeftWheelSpeed(0.06)
rob3.setRightWheelSpeed(0.03)

rob4 = FourWheelsRobot(300, 100, 0)
rob4.addComponent(led4)
rob4.setRightBackWheelSpeed(0.03)
rob4.setRightFrontWheelSpeed(0.08)
rob4.setLeftBackWheelSpeed(0.05)
rob4.setLeftFrontWheelSpeed(0.02)

env = Environment()

env.addObject(rob1)
env.addObject(rob2)
env.addObject(rob3)
env.addObject(rob4)

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
        led4.setState(ledState)
        start=time.time()
    if i==800:
        rob1.setLeftWheelSpeed(0.02)
        rob1.setLeftWheelCCW()

    # MSO TODO (Objectif) : Déplacer ces appels dans la simulation
    rob1.move()
    rob2.move()
    rob3.move()
    rob4.move()
    time.sleep(.02)
    i+=1