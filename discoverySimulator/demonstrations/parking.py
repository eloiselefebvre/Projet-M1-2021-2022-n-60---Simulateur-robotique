import time

from discoverySimulator import Object
from discoverySimulator.actuators import LED
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Line, Rectangle
from discoverySimulator.robots import FourWheelsRobot, RectangleTwoWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation

def parkingDemo():

    envWidth=800
    envHeight=800
    env=Environment(envWidth,envHeight)

    robot = FourWheelsRobot()
    env.addObject(robot,200,200,90)
    robot2=RectangleTwoWheelsRobot()
    env.addObject(robot2,100,100,90)
    floor=Object(Representation(Rectangle(envWidth,envHeight,"#999999")))
    env.addVirtualObject(floor,envWidth/2,envHeight/2)

    lines=[]
    telemeters=[]
    redLeds=[]
    greenLeds=[]

    for i in range(4):
        lines.append(Object(Representation(Line(100,4,"#fff"))))
        env.addVirtualObject(lines[i],envWidth-100,200+i*100,-90)

    for i in range(3):
        telemeters.append(Telemeter("#f00"))
        env.addObject(telemeters[i],envWidth-4,250+i*100,90)

    for i in range(3):
        redLeds.append(LED(LED.RED))
        env.addObject(redLeds[i],envWidth+10,233+i*100)

    for i in range(3):
        greenLeds.append(LED(LED.GREEN))
        env.addObject(greenLeds[i],envWidth+10,263+i*100)


    sim=Simulation(env)
    sim.showInterface()
    sim.run()

    while True:

        for i in range(3):
            if telemeters[i].getValue() < 100:
                redLeds[i].setState(LED.HIGH)
                greenLeds[i].setState(LED.LOW)
            else:
                greenLeds[i].setState(LED.HIGH)
                redLeds[i].setState(LED.LOW)


        time.sleep(.01)

