from PyQt5.QtWidgets import QSlider
from robotSimulator import Object
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Line
from robotSimulator import Pose
from screeninfo import get_monitors

class Environment:

    DEFAULT_BORDER_SCREEN_COLOR = "#717D95"
    DEFAULT_BORDER_SCREEN_WIDTH = 5

    def __init__(self):
        self._objects=[]
        screenWidth = get_monitors()[0].width
        screenHeight = get_monitors()[0].height
        self.addObject(Object(Representation(Line(screenHeight,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),100,0)
        self.addObject(Object(Representation(Line(screenHeight,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),screenWidth,0)
        self.addObject(Object(Representation(Line(screenWidth,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,0,-90)
        self.addObject(Object(Representation(Line(screenWidth,self.DEFAULT_BORDER_SCREEN_WIDTH,self.DEFAULT_BORDER_SCREEN_COLOR))),0,800,-90)
        # TODO : Trouver comment récupérer la taille de la fenêtre PyQt

    def addObject(self,obj,x,y,orientation=0):
        if isinstance(obj, Object):
            obj.setPose(Pose(x,y,orientation))
            obj.setEnv(self)
            self._objects.append(obj)

    def getObjects(self):
        return self._objects

    def addSlider(self,slider,x,y):
        if isinstance(slider,QSlider):
            slider.setEnv(self)
            slider.setPose(Pose(1000,1000))


