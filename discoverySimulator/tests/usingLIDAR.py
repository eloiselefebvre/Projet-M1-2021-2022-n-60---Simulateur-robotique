from PyQt5.QtCore import QPoint

from discoverySimulator import Obstacle
from discoverySimulator.obstacles.CircularObstacle import CircularObstacle
from discoverySimulator.obstacles.RectangularObstacle import RectangularObstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes.Polygon import Polygon
from discoverySimulator.robots.CircularTwoWheelsRobot import CircularTwoWheelsRobot
from discoverySimulator.robots.RectangularTwoWheelsRobot import RectangularTwoWheelsRobot
from discoverySimulator.sensors import LIDAR
from discoverySimulator.simulation import Environment, Simulation


def LIDARTest():
    lidar = LIDAR()
    rob = CircularTwoWheelsRobot()
    rob.addComponent(lidar)
    rob.setRightWheelSpeed(400)
    rob.setLeftWheelSpeed(400)

    lidar2 = LIDAR(accuracy=0.99)
    rob2 = RectangularTwoWheelsRobot()
    rob2.addComponent(lidar2)
    rob2.setRightWheelSpeed(200)
    rob2.setLeftWheelSpeed(400)

    env = Environment(1500, 900,'real')
    # env.addObject(rob, 400, 500)
    env.addObject(rob2, 900, 500)
    env.addObject(CircularObstacle(40, "#ff8fff"), 150, 180)
    env.addObject(RectangularObstacle(40, 200, "#ff8fff"), 650, 400)
    env.addObject(RectangularObstacle(400, 100, "#ff8fff"), 250, 850, 25)
    pol=Polygon([(500,500),(600,400),(800,400),(600,500),(800,700)],"#ff8fff")
    env.addObject(Obstacle(Representation(pol)))

    sim = Simulation(env)
    sim.run()
    sim.showInterface()