# Robotic simulator for Python

## What's this
**discoverySimulator** is a Python package where an environment can be simulate with some robots and sensors. This simulator aims to introduce robotics while taking your first steps in python. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the package  **discoverySimulator**:

```bash
$ pip install discoverySimulator
```

## Usage example

### Code
```python
from discoverySimulator.simulation import Simulation, Environment
from discoverySimulator.robots import RectangularTwoWheelsRobot

# Create robot and assign wheels speed
myRobot = RectangularTwoWheelsRobot()
myRobot.setRightWheelSpeed(500)
myRobot.setLeftWheelSpeed(200)

# Create environment
environmentWidth = 1500
environmentHeight = 1500
myEnvironment = Environment(environmentWidth,environmentHeight)
myEnvironment.addObject(myRobot,200,200,90)

# Create and run simulation 
mySimulation = Simulation(myEnvironment)
mySimulation.run()
mySimulation.showInterface()
```
### Code result 
![screenshot](output.png)


## License
[MIT](https://choosealicense.com/licenses/mit/)

## Help and bug reports
General questions and comments can be sent to the following email address: [discoverysimulator@gmail.com](mailto:discoverysimulator@gmail.com).

You can also report bugs at this same email address.