from discoverySimulator import Obstacle, Object
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle, Point, Line
from discoverySimulator.robots import RectangleTwoWheelsRobot

from discoverySimulator.simulation import Environment, Simulation

def odometryTesting():
    rob = RectangleTwoWheelsRobot()
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
