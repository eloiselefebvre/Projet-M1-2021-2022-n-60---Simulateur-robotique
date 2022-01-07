import random

from PyQt5.QtGui import QPainter

from Object import Object
from Point import Point
from Rectangle import Rectangle


class Robot(Object):

    def __init__(self,x,y,width,height,orientation):
        COLORS = ["#FFC465","#56D1BC","#675BB5","#F56E21","#0490F9","#FFCCCC","#CC6666","#9933FF","#66CC00","#3366CC"]
        super().__init__(x,y,width,height,orientation,Rectangle(Point(x,y),width,height,orientation,random.choice(COLORS)))
        self._wheelSet=[]

    def attachSensor(self,x,y,orientation): # repère local
        pass


    def draw(self,window):
        painter = QPainter(window)
        self._representation.draw(painter)
