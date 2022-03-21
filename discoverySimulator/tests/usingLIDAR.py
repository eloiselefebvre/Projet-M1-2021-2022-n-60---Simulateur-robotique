from PyQt5.QtCore import QPoint

from discoverySimulator import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle, Rectangle
from discoverySimulator.representation.shapes.Polygon import Polygon
from discoverySimulator.robots.CircleTwoWheelsRobot import CircleTwoWheelsRobot
from discoverySimulator.robots.RectangleTwoWheelsRobot import RectangleTwoWheelsRobot
from discoverySimulator.sensors import LIDAR
from discoverySimulator.simulation import Environment, Simulation


def LIDARTest():
    lidar = LIDAR()
    rob = CircleTwoWheelsRobot()
    rob.addComponent(lidar)
    rob.setRightWheelSpeed(400)
    rob.setLeftWheelSpeed(400)

    lidar2 = LIDAR()
    rob2 = RectangleTwoWheelsRobot()
    rob2.addComponent(lidar2)
    rob2.setRightWheelSpeed(200)
    rob2.setLeftWheelSpeed(400)

    env = Environment(1500, 900)
    env.addObject(rob, 400, 500)
    env.addObject(rob2, 900, 500)
    env.addObject(Obstacle(Representation(Circle(40, "#ff8fff"))), 150, 180)
    env.addObject(Obstacle(Representation(Rectangle(40, 200, "#ff8fff"))), 650, 400)
    env.addObject(Obstacle(Representation(Rectangle(400, 100, "#ff8fff"))), 250, 850, 25)
    env.addObject(Obstacle(Representation(Polygon([(500,500),(600,400),(800,400),(600,500),(800,700)], "#ff8fff"))))
    # env.addObject(LIDAR(),50,50)

    sim = Simulation(env)
    sim.setAcceleration(1)
    sim.run()
    sim.showInterface()

