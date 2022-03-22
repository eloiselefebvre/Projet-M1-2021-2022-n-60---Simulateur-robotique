import random
import time


class ReinforcementLearning:

    def __init__(self,state):
        """
        This method allows to create a reinforcement learning
        :param state: state of the robot who will learn
        """
        self._QTable={}
        self._minimalSpeed = 0
        self._maximalSpeed = 600
        self._numberOfInterval = 2
        self._step = int((self._maximalSpeed - self._minimalSpeed) / self._numberOfInterval)
        self.fillQTable()
        self._learningFactor = 0.1
        self._discountFactor = 0.9
        self._state = state
        self._initialState = state
        self._explorationRate=0.01
        self._tab=[0,0,0,0,0]
        self._actions = [(self._step,0),(-self._step,0),(0,self._step),(0,-self._step),(0,0)]
        self._actionToExecuteIndex=4

    def getReachableStates(self, state):
        actionIndices = self.getPossibleActions(state)
        reachableStates = []
        for actionIndex in actionIndices:
            reachableStates.append(self.getNextState(state, actionIndex))
        return reachableStates

    def getNextState(self, state, actionIndex):
        return (self._actions[actionIndex][0]+state[0],self._actions[actionIndex][1]+state[1])

    def fillQTable(self):
        for i in range(self._minimalSpeed, self._maximalSpeed + self._step, self._step):
            for j in range(self._minimalSpeed, self._maximalSpeed + self._step, self._step):
                self._QTable[(i, j)] = [0, 0, 0, 0, 0]      # MSO TODO : revoir ces valeurs en dur, à générer automatiquement

    def executedActionFeedback(self,reward):
        nextState=self.getNextState(self._state,self._actionToExecuteIndex)
        self._QTable[self._state][self._actionToExecuteIndex] = (1 - self._learningFactor) * self._QTable[self._state][self._actionToExecuteIndex] + self._learningFactor * (reward+self._discountFactor*max([self._QTable[nextState][index] for index in self.getPossibleActions(nextState)]))
        self._state = nextState

    def getPossibleActions(self, state = None):
        """
        This method allows to get the possible actions of the robot
        :param state: state of the robot
        :return: possible actions
        """
        state = state if state is not None else self._state
        actions = []
        if state[0]+self._step<=self._maximalSpeed:
            actions.append(0)
        if state[0]-self._step>=self._minimalSpeed:
            actions.append(1)
        if state[1]+self._step<=self._maximalSpeed:
            actions.append(2)
        if state[1]-self._step>=self._minimalSpeed:
            actions.append(3)
        actions.append(4)
        return actions

    def getActionToExecute(self):
        possibleActionsIndexes=self.getPossibleActions()
        if random.random() < self._explorationRate:
            minValue=self._tab[possibleActionsIndexes[0]]
            self._actionToExecuteIndex=possibleActionsIndexes[0]
            for index in possibleActionsIndexes:
                if self._tab[index]<minValue:
                    self._actionToExecuteIndex=index
                    minValue = self._tab[index]
        else:
            maxIndex=possibleActionsIndexes[0]
            max=self._QTable[self._state][maxIndex]
            for index in possibleActionsIndexes:
                if self._QTable[self._state][index]>max:
                    max = self._QTable[self._state][index]
                    maxIndex=index
            self._actionToExecuteIndex = maxIndex
        self._tab[self._actionToExecuteIndex]+=1
        return self._actions[self._actionToExecuteIndex]

    def reset(self):
        self._state=self._initialState
