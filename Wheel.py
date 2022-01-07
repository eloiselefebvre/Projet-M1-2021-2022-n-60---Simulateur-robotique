class Wheel:

    def __init__(self,diameter,representation):
        self._diameter = diameter
        self._speed = 0

    def setSpeed(self,speed):
        self._speed = speed

    def increaseSpeed(self,dSpeed):
        self._speed+=dSpeed

    def decreaseSpeed(self,dSpeed):
        self._speed-=dSpeed

    def draw(self,window):
        pass
