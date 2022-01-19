from robotSimulator.actuators.Actuator import Actuator
from robotSimulator.Representation import Representation
from robotSimulator.Circle import Circle

#import pygame.midi as pm

class Buzzer(Actuator):

    def __init__(self,x,y):
        super().__init__(x,y,0,Representation(Circle(5,"#1C1E32")))

    def on(self,midi_note):
        pass

    def off(self):
        pass