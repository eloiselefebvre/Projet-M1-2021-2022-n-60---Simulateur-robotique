import time

from discoverySimulator.actuators import LED
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation


def firstDemonstration():

    myRobot = RectangularTwoWheelsRobot()
    led = LED()

    environment = Environment(800,800)
    environment.addObject(myRobot,100,100,-90)

    simulation = Simulation(environment)
    simulation.run()
    simulation.showInterface()

    time.sleep(4)
    myRobot.addComponent(led,0,0)

    time.sleep(4)
    telemeter1 = Telemeter("#00f")
    telemeter2 = Telemeter("#00f")
    firstTime = 0
    clock = 0
    counter = 0
    offset = 4
    distance = 200
    ledState = 0


    while True:
        environment.addObject(telemeter1,300,2)
        environment.addObject(telemeter2,500,2)
        myRobot.setLeftWheelSpeed(400)
        myRobot.setRightWheelSpeed(400)

        if telemeter1.getValue()<800-offset and counter == 0:
            firstTime=simulation.time()
            counter+=1
            print("First Time !")
        elif telemeter2.getValue()<800-offset and counter == 1:
            secondTime=simulation.time()
            counter+=1
            print("Second Time !")
            clock = secondTime - firstTime

        if clock != 0 and counter == 2:
            speed = distance/clock
            counter+=1
            print("speed:",speed,"px/s")

        ledState=not ledState
        led.setState(ledState)

        simulation.sync()


