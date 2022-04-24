import time
from discoverySimulator.robots import FourWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation


def measureSpeedWithTelemeters():

    envHeight = 1000
    env=Environment(1500,1000)
    sim = Simulation(env)
    robot = FourWheelsRobot()
    env.addObject(robot,200,200,-90)
    robot.setRightWheelSpeed(200)
    robot.setLeftWheelSpeed(200)

    offset = 4
    telemeter1=Telemeter()
    positionTelemeter1=500
    env.addObject(telemeter1,positionTelemeter1,offset)
    telemeter2=Telemeter()
    positionTelemeter2=600
    env.addObject(telemeter2,positionTelemeter2,offset)

    sim.run()
    sim.showInterface()

    distance = positionTelemeter2-positionTelemeter1
    firstTime = 0
    clock = 0
    counter = 0 # State machine


    while True :

        if telemeter1.getValue()<envHeight-offset and counter == 0:
            firstTime=sim.time()
            counter+=1
            print("First Time !")
        elif telemeter2.getValue()<envHeight-offset and counter == 1:
            secondTime=sim.time()
            counter+=1
            print("Second Time !")
            clock = secondTime - firstTime

        if clock != 0 and counter == 2:
            speed = distance/clock
            counter+=1
            print("speed:",speed,"px/s")

        time.sleep(.01)





