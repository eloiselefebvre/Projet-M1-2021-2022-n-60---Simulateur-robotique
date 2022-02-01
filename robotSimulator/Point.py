class Point:

    def __init__(self,x,y):
        self._x = x
        self._y = y

    def __str__(self):
        return "("+str(self._x)+","+str(self._y)+")"

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def setY(self,y):
        self._y = y
        
    def move(self,x,y):
        self._x=x
        self._y=y