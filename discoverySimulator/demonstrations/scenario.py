import time

from discoverySimulator import Object, Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Rectangle, Circle, Polygon
from discoverySimulator.ressources.ReinforcementLearning import ReinforcementLearning
from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.robots import RectangularTwoWheelsRobot, CircularTwoWheelsRobot
from discoverySimulator.actuators import LED

def scenario():
    scenario1()
    scenario2()
    scenario3()

def scenario1():
    timeSleep = 6

    myEnvironment = Environment(600, 600)

    # 1
    myRobot = RectangularTwoWheelsRobot("#F9886A")
    myEnvironment.addObject(myRobot, 50, 300, -90)

    # 2
    myLed = LED(LED.YELLOW)
    myLed.setState(True)
    myLed.setVisible(False)

    # 3
    myTelemeter = Telemeter()
    myTelemeter.setVisible(False)

    # 4
    availableLED = LED(LED.GREEN)
    availableLED.setState(True)
    unavailableLED = LED(LED.RED)
    envTelemeter = Telemeter("#ff0",80)
    background = Object(Representation(Rectangle(myEnvironment.getWidth(),myEnvironment.getHeight(),"#21212F")))
    parkingLeftLine = Object(Representation(Rectangle(100,8,"#fff")))
    parkingRightLine = Object(Representation(Rectangle(100,8,"#fff")))

    myRobot.addComponent(myLed, 0, 0)
    myRobot.addComponent(myTelemeter, 0, 26)

    myEnvironment.addVirtualObject(background,myEnvironment.getWidth()/2,myEnvironment.getHeight()/2)
    myEnvironment.addVirtualObject(parkingLeftLine,550,260)
    myEnvironment.addVirtualObject(parkingRightLine,550,340)
    myEnvironment.addVirtualObject(availableLED,565,240)
    myEnvironment.addVirtualObject(unavailableLED,585,240)
    myEnvironment.addObject(envTelemeter,575,260)

    background.setVisible(False)
    parkingLeftLine.setVisible(False)
    parkingRightLine.setVisible(False)
    availableLED.setVisible(False)
    unavailableLED.setVisible(False)
    envTelemeter.setVisible(False)

    mySimulation = Simulation(myEnvironment)
    mySimulation.showInterface()
    mySimulation.run()

    mySimulation.sleep(timeSleep)
    myLed.setVisible(True)

    mySimulation.sleep(timeSleep)
    myTelemeter.setVisible(True)

    mySimulation.sleep(timeSleep)
    background.setVisible(True)
    parkingLeftLine.setVisible(True)
    parkingRightLine.setVisible(True)
    availableLED.setVisible(True)
    unavailableLED.setVisible(True)
    envTelemeter.setVisible(True)

    mySimulation.sleep(timeSleep)

    startTime = mySimulation.time()

    while mySimulation.time()<120:
        currentTime = mySimulation.time()
        if currentTime - startTime > 0.5:
            startTime = currentTime
            myLed.toggleState()

        if myTelemeter.getValue() < 20:
            myRobot.setLeftWheelSpeed(0)
            myRobot.setRightWheelSpeed(0)
            myLed.setState(LED.HIGH)
        else:
            myRobot.setLeftWheelSpeed(400)
            myRobot.setRightWheelSpeed(400)

        if envTelemeter.getValue() < 20 :
            availableLED.setState(False)
            unavailableLED.setState(True)
        else:
            availableLED.setState(True)
            unavailableLED.setState(False)

        mySimulation.sync()
    mySimulation.stop()
    mySimulation.closeInterface()

def scenario2():
    myRobot = CircularTwoWheelsRobot()

    environment = Environment(800,800)
    mySimulation = Simulation(environment)

    environment.addObject(myRobot,70,70,-90)
    environment.addObject(Obstacle(Representation(Circle(70,"#33FF9E"))),650,200)
    environment.addObject(Obstacle(Representation(Circle(50,"#F8FF00"))),100,280)
    environment.addObject(Obstacle(Representation(Circle(100,"#FF8700"))),220,620)
    environment.addObject(Obstacle(Representation(Rectangle(400,30,"#FF33F7"))),202,200)
    environment.addObject(Obstacle(Representation(Polygon([(800,200),(600,300),(500,200)],"#BDB9E6"))),-86,234)

    mySimulation.run()
    mySimulation.showInterface()

    while mySimulation.time()<60:
        mySimulation.sync()

    mySimulation.stop()
    mySimulation.closeInterface()

def scenario3():
    env = Environment(1500, 1500)
    robot = RectangularTwoWheelsRobot()
    env.addObject(robot, 500, 400, -90)

    sim = Simulation(env)
    sim.run()
    sim.showInterface()

    initialPose = robot.getPose().copy()
    currentState = (robot.getLeftWheel().getSpeed(), robot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState)

    timeLearning = 10
    start = sim.time()

    while True:
        current = sim.time()
        if current - start < timeLearning:
            startPosition = (robot.getPose().getX(), robot.getPose().getY())
            startOrientation = robot.getPose().getOrientation()
            startOrientation %= 360

            # action during 0.1 second to see the result of the action
            action = reinforcementLearning.getActionToExecute()
            robot.setRightWheelSpeed(robot.getRightWheel().getSpeed() + action[0])
            robot.setLeftWheelSpeed(robot.getLeftWheel().getSpeed() + action[1])

            sim.sleep(0.2)

            endPosition = (robot.getPose().getX(), robot.getPose().getY())
            endOrientation = robot.getPose().getOrientation()

            distance = ((endPosition[0] - startPosition[0]) ** 2 + (endPosition[1] - startPosition[1]) ** 2)**0.5

            reward = distance / (1 + (endOrientation - startOrientation) ** 2)  # encourages to go straight
            # reward = (endOrientation-startOrientation)/(distance+1) # encourages to turn
            reinforcementLearning.learn(reward)

        else:
            start = sim.time()
            robot.setPose(initialPose.copy())
            robot.setLeftWheelSpeed(0)
            robot.setRightWheelSpeed(0)
            robot.setCollidedState(False)
            reinforcementLearning.reset()

        sim.sync()
