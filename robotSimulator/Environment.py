from Object import Object


class Environment:

    def __init__(self,):
        self._objects=[]

    def addObject(self, obj):
        if isinstance(obj, Object):
            self._objects.append(obj)

    def getObjects(self):
        return self._objects