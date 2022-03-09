from robotSimulator import Obstacle, Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Circle, Point, Line
from robotSimulator.robots import TwoWheelsRobot

from robotSimulator.simulation import Environment, Simulation

def odometryTesting():
    rob = TwoWheelsRobot()
    rob.setRightWheelSpeed(400) # avec 400 : dteta = 0.7639437268410916 degré

    env = Environment(1500, 900)
    env.addObject(rob,500,500)
    env.addVirtualObject(Object(Representation(Point(500,500,'#0f0'))))
    env.addVirtualObject(Object(Representation(Point(525,500))))
    env.addVirtualObject(Object(Representation(Point(550,500,"#f00"))))
    env.addVirtualObject(Object(Representation(Line(25,2,"#f00"))),550,500)
    env.addVirtualObject(Object(Representation(Line(25,2,"#f00"))),550,500,-90)
    env.addVirtualObject(Object(Representation(Line(25,2,"#f00"))),550,500,-180)
    env.addVirtualObject(Object(Representation(Line(25,2,"#f00"))),550,500,90)
    env.addVirtualObject(Object(Representation(Line(25,2,"#f00"))),550,500,135)
    env.addVirtualObject(Object(Representation(Line(25,2,"#f00"))),550,500,45)
    env.addVirtualObject(Object(Representation(Line(25,2,"#f00"))),550,500,-45)
    env.addVirtualObject(Object(Representation(Line(50,2,"#f00"))),550,500,-135)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()
