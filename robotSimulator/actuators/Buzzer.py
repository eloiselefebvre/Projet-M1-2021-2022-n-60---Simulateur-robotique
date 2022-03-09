from . import Actuator
from robotSimulator.representation import Representation
from robotSimulator.representation.shapes import Circle

#import pygame.midi as pm

class Buzzer(Actuator):

    def __init__(self):
        super().__init__(Representation(Circle(5,"#1C1E32")))

    def on(self,midi_note):
        pass

    def off(self):
        pass

    def getSpecifications(self):
        return ""