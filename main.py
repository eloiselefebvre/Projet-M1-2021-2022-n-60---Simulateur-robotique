# # from discoverySimulator.demonstrations import roadDemo
# # roadDemo()
#
# from discoverySimulator.tests import aStar, collisionAndTelemeter, usingLIDAR, reinforcementLearning, \
#     reinforcementLearningTest, rlTwoWheelsRobot, rlAvoiding, rlFourWheelsRobot,road
#
# # aStar()
# # collisionAndTelemeter()
# # usingLIDAR.LIDARTest()
# # reinforcementLearningTest()
# # rlTwoWheelsRobot.reinforcementLearningTest()
# # rlAvoiding.reinforcementLearningTest()
# road.road()
from discoverySimulator.ressources.maps.Maze import Maze
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
Maze(myEnvironment)

# create and run simulation
mySimulation = Simulation(myEnvironment)
mySimulation.run()
mySimulation.showInterface()