from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.actuators import LED


def scenario():
    myLed = LED(LED.YELLOW)
    # myLed.setVisible(False)

    myTelemeter = Telemeter()
    myTelemeter.setVisible(False)

    myRobot = RectangularTwoWheelsRobot("#F9886A")
    myRobot.addComponent(myLed, 0, 0)
    myRobot.addComponent(myTelemeter, 0, 26)

    myEnvironment = Environment(600, 600)
    myEnvironment.addObject(myRobot, 50, 300, -90)

    mySimulation = Simulation(myEnvironment)
    mySimulation.showInterface()
    mySimulation.run()

    startTime = mySimulation.time()
    while True:
        currentTime = mySimulation.time()

        if currentTime > 4:
            myLed.setVisible(True)
            # myRobot.addComponent(myLed, 0, 0)
            if currentTime - startTime > 0.5:
                startTime = currentTime
                myLed.toggleState()

        if currentTime > 8:
            myTelemeter.setVisible(True)

        if currentTime > 12:
            if myTelemeter.getValue() < 20:
                myRobot.setLeftWheelSpeed(0)
                myRobot.setRightWheelSpeed(0)
                myLed.setState(LED.HIGH)
            else:
                myRobot.setLeftWheelSpeed(500)
                myRobot.setRightWheelSpeed(500)

        mySimulation.sync()
