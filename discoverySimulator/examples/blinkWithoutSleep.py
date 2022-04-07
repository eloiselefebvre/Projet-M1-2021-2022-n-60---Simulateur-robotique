from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.actuators import LED

def blinkWithoutSleep():
    led = LED()
    rob = RectangularTwoWheelsRobot()

    environment = Environment(500,500)
    environment.addObject(led,environment.getWidth()/2,environment.getHeight()/2)
    environment.addObject(rob,100,100,-45)
    rob.setLeftWheelSpeed(200)
    rob.setRightWheelSpeed(200)

    simulation = Simulation(environment)
    simulation.showInterface()
    simulation.run()

    startTime = simulation.time()

    while True:
        currentTime = simulation.time()
        if currentTime - startTime >= 1:
            startTime = currentTime
            led.toggleState()

        simulation.sync()