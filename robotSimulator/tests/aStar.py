import time

from robotSimulator import Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line, Rectangle
from robotSimulator.ressources.maps.PathFinding import PathFinding
from robotSimulator.robots import TwoWheelsRobot
from robotSimulator.simulation import Environment, Simulation

def aStar():

    robot = TwoWheelsRobot(100)
    robot.setLeftWheelSpeed(150)
    robot.setRightWheelSpeed(150)

    envWidth = 1500
    envHeight = 1500
    env = Environment(envWidth,envHeight)
    # env.addObject(robot,200,200)
    numberOfColumns = 100
    numberofLines = 100
    #
    # startPositionX = int(robot.getPose().getX())
    # startPositionY = int(robot.getPose().getY())
    # startOrientation = robot.getPose().getOrientation()
    # previousStateX = int((startPositionX * numberOfColumns) / envWidth)
    # previousStateY = int((startPositionY * numberofLines) / envHeight)

    # points de départ et point d'arrivée
    beginNode = None
    endNode = None

    for i in range (numberofLines):
        env.addVirtualObject(Object(Representation(Line(envWidth, 1, "#000"))), 0, i*15, -90)
    for j in range (numberOfColumns):
        env.addVirtualObject(Object(Representation(Line(envWidth,1, "#000"))),j*15,0)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()
    PathFinding(env)

    # while True:
    #     robotCurrentPoseX = robot.getPose().getX()
    #     robotCurrentPoseY = robot.getPose().getY()
    #     currentStateX = int(robotCurrentPoseX * numberOfColumns / envWidth)
    #     currentStateY = int(robotCurrentPoseY * numberofLines / envHeight)
    #     print("current state:",currentStateX,currentStateY)
    #     env.addVirtualObject(Object(Representation(Rectangle(15,15,"#FF9900"))),(currentStateX*15+(currentStateX+1)*15)/2,(currentStateY*15+(currentStateY+1)*15)/2)
    #
    #
    #     time.sleep(.01)



