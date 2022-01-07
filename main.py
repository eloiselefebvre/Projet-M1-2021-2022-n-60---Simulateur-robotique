import random

from Environment import Environment
from Robot import Robot
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)
env = Environment()

for i in range(5):
    robot = Robot(random.randint(0, 1600), random.randint(0, 800), random.randint(40, 50), random.randint(50, 60),
                  random.randint(-90, 90))
    env.addObject(robot)

robot = Robot(random.randint(0, 1600), random.randint(0, 800), random.randint(40, 50), random.randint(50, 60), 0)
env.addObject(robot)

sys.exit(app.exec())

