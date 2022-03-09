from PyQt5.QtWidgets import QHBoxLayout, QMenuBar, QAction

from robotSimulator.ressources.maps.Maze import Maze
from robotSimulator.ressources.maps.CirclePath import CirclePath


class Header(QMenuBar):

    def __init__(self,environment):
        super().__init__()
        self._layout = QHBoxLayout()
        self._environment = environment
        self.setLayout(self._layout)
        self.setStyleSheet("background-color : #f9f9f9")
        self._mazeMenu = self.addMenu("Maze")
        self._pathMenu = self.addMenu("Circle Path")
        self._actionsMaze=[]
        self._actionsPath = []
        self.insertionMaze()
        self.insertionPath()
        self._maze=Maze(self._environment)
        self._path=CirclePath(self._environment)

    def insertionMaze(self):
        for action in self._actionsMaze:
            self._mazeMenu.removeAction(action)
        self._actionsMaze.clear()
        if self._environment.hasMaze():
            generateNewMaze=QAction("Generate new maze", self)
            self._mazeMenu.addAction(generateNewMaze)
            generateNewMaze.triggered.connect(self.generateNewMaze)
            self._actionsMaze.append(generateNewMaze)
            removeMaze=QAction("Remove maze",self)
            self._mazeMenu.addAction(removeMaze)
            removeMaze.triggered.connect(self.removeMaze)
            self._actionsMaze.append(removeMaze)
        else:
            generateMaze = QAction("Generate maze",self)
            self._mazeMenu.addAction(generateMaze)
            generateMaze.triggered.connect(self.generateMaze)
            self._actionsMaze.append(generateMaze)

    def insertionPath(self):
        for action in self._actionsPath:
            self._pathMenu.removeAction(action)
        self._actionsPath.clear()
        if self._environment.hasPath():
            generateNewPath=QAction("Generate new circle path", self)
            self._pathMenu.addAction(generateNewPath)
            generateNewPath.triggered.connect(self.generateNewPath)
            self._actionsPath.append(generateNewPath)
            removePath=QAction("Remove Path",self)
            self._pathMenu.addAction(removePath)
            removePath.triggered.connect(self.removePath)
            self._actionsPath.append(removePath)
        else:
            generatePath = QAction("Generate path",self)
            self._pathMenu.addAction(generatePath)
            generatePath.triggered.connect(self.generatePath)
            self._actionsPath.append(generatePath)

    def generateMaze(self):
        self._maze.drawGrid()
        self._environment.setMaze(True)
        self.insertionMaze()

    def generatePath(self):
        self._path.drawPath()
        self._environment.setPath(True)
        self.insertionPath()

    def removeMaze(self):
        freeObjects=[]
        for obj in self._environment.getObjects():
            for wall in self._maze.getWalls():
                if obj.isCollidedWith(wall):
                    freeObjects.append(obj)

        self._maze.deleteGrid()
        self._environment.setMaze(False)
        self.insertionMaze()

        for freeObject in freeObjects:
            freeObject.setCollidedState(False)

    def removePath(self):
        self._path.deleteElements()
        self._environment.setPath(False)
        self.insertionPath() # TODO : Revoir la suppression de tous les éléments

    def generateNewMaze(self):
        self.removeMaze()
        self.generateMaze()

    def generateNewPath(self):
        self.removePath()
        self.generatePath()


