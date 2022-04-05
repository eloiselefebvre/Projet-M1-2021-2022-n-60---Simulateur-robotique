from discoverySimulator import Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle, Rectangle, Polygon
from discoverySimulator.robots import CircularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation


def secondDemonstration():

    myRobot = CircularTwoWheelsRobot()

    environment = Environment(800,800)
    simulation = Simulation(environment)

    environment.addObject(myRobot,70,70,-90)
    environment.addObject(Obstacle(Representation(Circle(70,"#33FF9E"))),650,200)
    environment.addObject(Obstacle(Representation(Circle(50,"#F8FF00"))),100,280)
    environment.addObject(Obstacle(Representation(Circle(100,"#FF8700"))),220,620)
    environment.addObject(Obstacle(Representation(Rectangle(400,30,"#FF33F7"))),202,200)
    environment.addObject(Obstacle(Representation(Polygon([(500,200),(600,300),(800,200)],"#BDB9E6"))),-86,234)

    simulation.run()
    simulation.showInterface()