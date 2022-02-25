from robotSimulator import Obstacle
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Rectangle, Circle
import random


class Map():

    LARGEUR = 1000
    HAUTEUR = 1000
    NUMBER_OF_OBSTACLES = 20

    def __init__(self,environment):
        self._Obstacles=[]
        self._env = environment
        pass

    def generateObstaclesPositionX(self):
        positionX = random.randint(1,self.LARGEUR)
        return positionX

    def generateObstaclesPositionY(self):
        positionY = random.randint(1,self.HAUTEUR)
        return positionY

    def generateObstacleWidth(self):
        width=random.randint(1,50)
        return width

    def generateObstacleHeight(self):
        height=random.randint(1,500)
        return height

    def generateObstacleOrientation(self):
        rnd = random.Random()
        orientation = rnd.choice([0,90,-90])
        return orientation

    def generateObstacles(self):
        for i in range(self.NUMBER_OF_OBSTACLES):
            newObstacle = Obstacle(Representation(Rectangle(self.generateObstacleWidth(),self.generateObstacleHeight(),"#000")))
            self._env.addObject(newObstacle,self.generateObstaclesPositionX(),self.generateObstaclesPositionY(),self.generateObstacleOrientation())
            print(newObstacle)








