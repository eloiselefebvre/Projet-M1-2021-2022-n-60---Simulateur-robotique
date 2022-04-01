# discoverySimulator

discoverySimulator is a Python package where an environment can be simulate with some robots and sensors. This simulator aims to introduce robotics while taking your first steps in python. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install discoverySimulator:

```bash
pip install discoverySimulator
```

## Usage

### Code
```python
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.simulation import Simulation, Environment

# create robot and asign wheels speed
myRobot = RectangularTwoWheelsRobot()
myRobot.setRightWheelSpeed(500)
myRobot.setLeftWheelSpeed(200)

# create environment
environmentWidth = 1500
environmentHeight = 1500
myEnvironment = Environment(environmentWidth,environmentHeight)
myEnvironment.addObject(myRobot,200,200,90)

# create and run simulation 
mySimulation = Simulation(myEnvironment)
mySimulation.run()
mySimulation.showInterface()
```
### Output 
![](output.png)


## License
[MIT](https://choosealicense.com/licenses/mit/)