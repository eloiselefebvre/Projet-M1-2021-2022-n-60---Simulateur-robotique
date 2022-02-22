from robotSimulator import Object, Pose
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line
from screeninfo import get_monitors

class Environment:

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 5

    def __init__(self):
        self._objects=[]
        screenWidth = get_monitors()[0].width
        screenHeight = get_monitors()[0].height
        self.addObject(Object(Representation(Line(screenHeight,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,0)
        self.addObject(Object(Representation(Line(screenHeight,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),screenWidth,0)
        self.addObject(Object(Representation(Line(screenWidth,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),screenWidth,screenHeight,-90)
        self.addObject(Object(Representation(Line(screenWidth,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,screenHeight,-90)
        # TODO : Trouver comment récupérer la taille de la fenêtre PyQt

    def addObject(self,obj,x,y,orientation=0):
        if isinstance(obj, Object):
            obj.setPose(Pose(x,y,orientation))
            obj.setEnv(self)
            self._objects.append(obj)

    def getObjects(self):
        return self._objects




