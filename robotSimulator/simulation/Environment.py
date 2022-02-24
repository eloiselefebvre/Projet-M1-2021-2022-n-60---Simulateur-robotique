from robotSimulator import Object, Pose
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line
from screeninfo import get_monitors

class Environment:

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 1

    def __init__(self):
        self._objects=[]

    def addObject(self,obj,x=0,y=0,orientation=0):
        if isinstance(obj, Object):
            obj.setPose(Pose(x,y,orientation))
            obj.setEnv(self)
            self._objects.append(obj)

    def addObjectAtTheBack(self,obj,x=0,y=0,orientation=0):
        if isinstance(obj, Object):
            obj.setPose(Pose(x,y,orientation))
            obj.setEnv(self)
            self._objects.insert(0,obj)

    def removeObject(self,obj):
        if obj in self._objects:
            self._objects.remove(obj)


    def getObjects(self):
        return self._objects


    def drawWalls(self,width,height):
        self.addObject(Object(Representation(Line(height, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))), 0,0)
        self.addObject(Object(Representation(Line(height, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))),width, 0)
        self.addObject(Object(Representation(Line(width, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))), 0,0, -90)
        self.addObject(Object(Representation(Line(width, self.DEFAULT_BORDER_SCREEN_WIDTH, self.DEFAULT_BORDER_SCREEN_COLOR))), 0,height, -90)
        # TODO : Trouver comment récupérer la taille de la fenêtre PyQt
