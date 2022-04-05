from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.actuators import LED

def blink():
    led = LED()

    environment = Environment(500,500)
    environment.addObject(led,250,250)

    simulation = Simulation(environment)
    simulation.showInterface()
    simulation.run()

    while True:
        led.toggleState()
        simulation.sleep(1)

        simulation.sync()