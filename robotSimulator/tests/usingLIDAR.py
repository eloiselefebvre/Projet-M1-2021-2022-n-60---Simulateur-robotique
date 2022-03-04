from robotSimulator import Obstacle
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Circle, Rectangle
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.sensors import LIDAR
from robotSimulator.simulation import Environment, Simulation


def LIDARTest():
    lidar = LIDAR()
    rob = TwoWheelsRobot()
    rob.addComponent(lidar)
    rob.setRightWheelSpeed(400)
    rob.setLeftWheelSpeed(400)

    lidar2 = LIDAR("#00f")
    rob2 = TwoWheelsRobot()
    rob2.addComponent(lidar2)
    rob2.setRightWheelSpeed(200)
    rob2.setLeftWheelSpeed(400)

    env = Environment(1500, 900)
    env.addObject(rob, 500, 500)
    env.addObject(rob2, 900, 500)
    env.addObject(Obstacle(Representation(Circle(40, "#ff8fff"))), 150, 180)
    env.addObject(Obstacle(Representation(Rectangle(40, 200, "#ff8fff"))), 650, 400)
    env.addObject(Obstacle(Representation(Rectangle(400, 100, "#ff8fff"))), 250, 850, 25)

    sim = Simulation(env)
    sim.setAcceleration(1)
    sim.run()
    sim.showInterface()

