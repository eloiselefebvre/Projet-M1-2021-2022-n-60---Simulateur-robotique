from PyQt5.QtWidgets import QHBoxLayout, QMenuBar, QAction

from robotSimulator.ressources.maps.Maze import Maze


class Header(QMenuBar):

    def __init__(self,environment):
        super().__init__()
        self._layout = QHBoxLayout()
        self._environment = environment
        self.setLayout(self._layout)
        self.setStyleSheet("background-color : #f9f9f9")
        self._insertion = self.addMenu("Maze")
        self._actions=[]
        self.insertionMenu()
        self._maze=Maze(self._environment)

    def insertionMenu(self):
        for action in self._actions:
            self._insertion.removeAction(action)
        self._actions=[]
        if self._environment.hasMaze():
            generateNewMaze=QAction("Generate new maze", self)
            self._insertion.addAction(generateNewMaze)
            generateNewMaze.triggered.connect(self.generateNewMaze)
            self._actions.append(generateNewMaze)
            removeMaze=QAction("Remove maze",self)
            self._insertion.addAction(removeMaze)
            removeMaze.triggered.connect(self.removeMaze)
            self._actions.append(removeMaze)
        else:
            generateMaze = QAction("Generate maze",self)
            self._insertion.addAction(generateMaze)
            generateMaze.triggered.connect(self.generateMaze)
            self._actions.append(generateMaze)

    def generateMaze(self):
        self._maze.drawGrid()
        self._environment.setMaze(True)
        self.insertionMenu()

    def removeMaze(self):
        self._maze.deleteGrid()
        self._environment.setMaze(False)
        self.insertionMenu()

    def generateNewMaze(self):
        self.removeMaze()
        self.generateMaze()
