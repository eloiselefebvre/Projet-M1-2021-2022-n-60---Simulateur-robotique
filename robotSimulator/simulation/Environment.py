from robotSimulator import Object
from robotSimulator.representation.shapes import Point

class Environment:

    def __init__(self,):
        self._objects=[]

    def addObject(self,obj,x,y,orientation=0):
        if isinstance(obj, Object):
            obj.setParameters(Point(x,y),orientation)
            self._objects.append(obj)

    def getObjects(self):
        return self._objects


