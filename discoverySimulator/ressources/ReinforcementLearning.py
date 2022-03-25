import random
from typing import List


class ReinforcementLearning:

    # Available algorithm : QLearning, ValueIteration
    def __init__(self,state:tuple,algorithm:str="QLearning"):
        """
        This method allows to create a reinforcement learning
        :param state: state of the robot who will learn
        """
        self._learn = self.__getattribute__(f"_learn{algorithm}")
        self._QTable={}
        self._minimalSpeed = 0
        self._maximalSpeed = 600
        self._numberOfInterval = 2
        self._step = int((self._maximalSpeed - self._minimalSpeed) / self._numberOfInterval)
        self._learningFactor = 0.1
        self._discountFactor = 0.5
        self._state = state
        self._initialState = state
        self._explorationRate = 1
        self._explorationRateDecreaseFactor = 0.999
        self._actionCountTable = {}
        self._actions = [(self._step,0),(-self._step,0),(0,self._step),(0,-self._step),(0,0)]
        self.fillTable("_QTable")
        self.fillTable("_actionCountTable")

    # GETTERS
    def getReachableStates(self, state:tuple) -> List[tuple]:
        actionIndices = self.getPossibleActions(state)
        reachableStates = []
        for actionIndex in actionIndices:
            reachableStates.append(self.getNextState(state, actionIndex))
        return reachableStates

    def getNextState(self, state:tuple, actionIndex:int) -> tuple:
        return (self._actions[actionIndex][0]+state[0],self._actions[actionIndex][1]+state[1])

    def getPossibleActions(self, state:tuple = None) -> List[int]:
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

    def getActionToExecute(self) -> tuple:
        """
        This method allows to get the best action to execute
        :return: the action to execute
        """
        possibleActionsIndexes=self.getPossibleActions()
        if random.random() < self._explorationRate:
            actionWeights = self.computeActionWeights(self._state,possibleActionsIndexes)
            self._actionToExecuteIndex=random.choices(population=possibleActionsIndexes,weights=actionWeights,k=1)[0]
        else:
            maxIndex=possibleActionsIndexes[0]
            max=self._QTable[self._state][maxIndex]
            for index in possibleActionsIndexes:
                if self._QTable[self._state][index]>max:
                    max = self._QTable[self._state][index]
                    maxIndex=index
            self._actionToExecuteIndex = maxIndex

        return self._actions[self._actionToExecuteIndex]

    def computeActionWeights(self,state:tuple,possibleActionIndexes:List[int]) -> List[float]:
        penalisationFactor = 10
        possibleActionCounts = [(penalisationFactor*self._actionCountTable[state][i]+1) for i in possibleActionIndexes]
        total = sum(possibleActionCounts)
        return [(total-actionCount) / total for actionCount in possibleActionCounts]

    def fillTable(self,tableName:str,initValue=0):
        table = self.__getattribute__(tableName)
        for i in range(self._minimalSpeed, self._maximalSpeed + self._step, self._step):
            for j in range(self._minimalSpeed, self._maximalSpeed + self._step, self._step):
                table[(i, j)] = [initValue] * len(self._actions)

    def _learnQLearning(self,reward:float):
        """
        This method is used to execute the action chosen and to learn (QLearning)
        :param reward: the reward of the action
        """
        nextState=self.getNextState(self._state,self._actionToExecuteIndex)
        maxValue = max(self._QTable[nextState])
        self._QTable[self._state][self._actionToExecuteIndex] = (1 - self._learningFactor) * self._QTable[self._state][self._actionToExecuteIndex] + self._learningFactor * (reward+self._discountFactor*maxValue)
        self._actionCountTable[self._state][self._actionToExecuteIndex]+=1
        self._state = nextState

    def _learnValueIteration(self,reward:float):
        """
        This method is used to execute the action chosen and to learn (ValueIteration)
        :param reward: the reward of the action
        """

    def reset(self):
        self._state=self._initialState

    def learn(self,reward:float):
        self._explorationRate *= self._explorationRateDecreaseFactor
        self._learn(reward)

    def printTable(self,tableName:str):
        table=self.__getattribute__(tableName)
        print(f"----------{tableName}----------")
        for state in table:
            print(state,table[state])
        print("--------------------------------")
