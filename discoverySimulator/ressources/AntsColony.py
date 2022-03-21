import time


class AntsColony():

    INTERVAL_SIZE = 15

    def __init__(self,environment):
        self._environment=environment
        envWidth=self._environment.getWidth()
        envHeight=self._environment.getHeight()
        self.__ROWS_NUMBER = int((envWidth)/self.INTERVAL_SIZE)
        self.__COLS_NUMBER = int((envHeight)/self.INTERVAL_SIZE)
        self._grid={}

        for i in range(1,self.__COLS_NUMBER+1):
            for j in range(1,self.__ROWS_NUMBER+1):
                self._grid[(i,j)]=0

    def gridValues(self,robot):
        currentPosition=(robot.getPose().getX(),robot.getPose().getY())
        currentState=(int(currentPosition[0]/15),int(currentPosition[1]/15))
        self._grid[(currentState[0],currentState[1])]+=1












