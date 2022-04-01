# discoverySimulator

discoverySimulator is a Python package 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install discoverySimulator.

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

# create and run simulation 
mySimulation = Simulation(myEnvironment)
mySimulation.run()
mySimulation.showInterface()
```
### Output 



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)