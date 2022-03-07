from robotSimulator.Object import Object

class Component(Object):
    def __init__(self,representation):
        super().__init__(representation)
        self._parent = None

    def setParent(self,parent):
        self._parent = parent


