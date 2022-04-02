from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.actuators import LED

def blinkWithoutSleep():
    led = LED()

    environment = Environment(500,500)
    environment.addObject(led,250,250)

    simulation = Simulation(environment)
    simulation.showInterface()
    simulation.run()

    startTime = simulation.time()

    while simulation.time()<5:
    # while True:
        currentTime = simulation.time()
        if currentTime - startTime >= 1:
            startTime = currentTime
            led.toggleState()

        simulation.sync()

    simulation.stop()
    # simulation.sleep(2)
    # simulation.closeInterface()

