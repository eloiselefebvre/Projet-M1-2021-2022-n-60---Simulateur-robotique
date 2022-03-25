import random
from typing import List


class ReinforcementLearning:

    DEFAULT_LEARNING_FACTOR = 0.1
    DEFAULT_DISCOUNT_FACTOR = 0.5
    DEFAULT_EXPLORATION_RATE_DECREASE_FACTOR = 0.995

    # Available algorithm : QLearning, ValueIteration
    def __init__(self, state:tuple, factors=None, algorithm:str= "ValueIteration"):
        # TODO : Rendre plus modulable et revoir e-greedy exploration
        """ This method allows to create a reinforcement learning
        @param state  State of the robot who will learn
        """

        self._learn = self.__getattribute__(f"_learn{algorithm}")

        if factors is None:
            factors = {}
        self._factors={
            'learning':ReinforcementLearning.DEFAULT_LEARNING_FACTOR,
            'discount':ReinforcementLearning.DEFAULT_DISCOUNT_FACTOR,
            'explorationRateDecrease':ReinforcementLearning.DEFAULT_EXPLORATION_RATE_DECREASE_FACTOR
        }
        self._factors.update(factors)

        self._explorationRate = 1


        self._minimalSpeed = 0
        self._maximalSpeed = 600
        self._numberOfInterval = 2
        self._step = int((self._maximalSpeed - self._minimalSpeed) / self._numberOfInterval)

        self._state = state
        self._initialState = state
        self._actions = [(self._step,0),(-self._step,0),(0,self._step),(0,-self._step),(0,0)]

        self._QTable={}
        self._RTable={}
        self._actionCountTable = {}
        self.fillTable("_QTable")
        self.fillTable("_RTable")
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
        """ This method allows to get the possible actions of the robot
        @param state  State of the robot
        @return  Possible actions
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
        """ This method allows to get the best action to execute
        @return  The action to execute
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

    def printTable(self,tableName:str):
        table=self.__getattribute__(tableName)
        print(f"----------{tableName}----------")
        for state in table:
            print(state,table[state])
        print("--------------------------------")

    def learn(self,reward:float):
        self._explorationRate *= self._factors["explorationRateDecrease"]
        self._learn(reward)
        self._actionCountTable[self._state][self._actionToExecuteIndex]+=1

    def _learnQLearning(self,reward:float):
        """ This method is used to execute the action chosen and to learn (QLearning)
        @param reward  The reward of the action
        """
        nextState=self.getNextState(self._state,self._actionToExecuteIndex)
        maxValue = max(self._QTable[nextState])
        self._QTable[self._state][self._actionToExecuteIndex] = (1 - self._factors["learning"]) * self._QTable[self._state][self._actionToExecuteIndex] + self._factors["learning"] * (reward+self._factors["discount"]*maxValue)
        self._state = nextState

    def _learnValueIteration(self,reward:float):
        """ This method is used to execute the action chosen and to learn (ValueIteration)
        @param reward  The reward of the action
        """
        # reward update
        actionCount = self._actionCountTable[self._state][self._actionToExecuteIndex]
        oldReward = self._RTable[self._state][self._actionToExecuteIndex]
        self._RTable[self._state][self._actionToExecuteIndex] = (reward+actionCount*oldReward)/(actionCount+1)

        # value iteration
        for state in self._QTable.keys():
            for actionIndex in self.getPossibleActions(state):
                newState = self.getNextState(state,actionIndex)
                maxValue = max(self._QTable[newState])
                reward = self._RTable[state][actionIndex]
                self._QTable[state][actionIndex]=reward+self._factors["discount"]*maxValue
        self._state = self.getNextState(self._state,self._actionToExecuteIndex)
        self._actionCountTable[self._state][self._actionToExecuteIndex] += 1

    def reset(self):
        self._state=self._initialState
