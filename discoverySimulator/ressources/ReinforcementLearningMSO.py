import random


class ReinforcementLearning:

    # Available algorithms = ValueIteration, QLearning
    def __init__(self,state, algorithm = "ValueIteration"):

        self._learn = self.__getattribute__(f"_learn{algorithm}")  # raises an error if not found
        self._minimalSpeed = 0
        self._maximalSpeed = 600
        self._numberOfInterval = 2
        self._step = int((self._maximalSpeed - self._minimalSpeed) / self._numberOfInterval)
        self._learningFactor = 0.1
        self._discountFactor = 0.5
        self._explorationRateDecreaseFactor = 0.995
        self._state = state
        self._initialState = state
        self._explorationRate=1
        self._actions = [(self._step,0),(-self._step,0),(0,self._step),(0,-self._step),(0,0)]
        self._QTable = {}
        self._RTable = {}
        self._actionCount = {}
        self.fillTable("_QTable")
        self.fillTable("_RTable")
        self.fillTable("_actionCount")

    def fillTable(self, tableName, initValue = 0):
        table = self.__getattribute__(tableName)
        for i in range(self._minimalSpeed, self._maximalSpeed + self._step, self._step):
            for j in range(self._minimalSpeed, self._maximalSpeed + self._step, self._step):
                table[(i, j)] = [initValue]  * len(self._actions)



    def getNextState(self, state, actionIndex):
        return (self._actions[actionIndex][0]+state[0],self._actions[actionIndex][1]+state[1])

    def getState(self):
        return self._state

    def printQTable(self):
        self.printTable("_QTable")

    def printTable(self, tableName):
        table = self.__getattribute__(tableName)
        # print(f"----------{tableName}---------------")
        for state in table:
            print(state, table[state])
        # print(f"------------------------------------")

    def learn(self, reward):
        self._learn(reward)

    def _learnQLearning(self, reward):

        self._explorationRate *= self._explorationRateDecreaseFactor
        # print("exploration rate : ", self._explorationRate)

        nextState = self.getNextState(self._state, self._actionToExecuteIndex)
        maxValue = max(self._QTable[nextState])
        self._QTable[self._state][self._actionToExecuteIndex] = (1 - self._learningFactor) * self._QTable[self._state][self._actionToExecuteIndex] + self._learningFactor * (reward + self._discountFactor * maxValue)
        self._actionCount[self._state][self._actionToExecuteIndex] += 1
        self._state = nextState
        self.printQTable()

    def _learnValueIteration(self,reward):

        self._explorationRate *= self._explorationRateDecreaseFactor
        # print("exploration rate : ", self._explorationRate)

        # reward update
        actionCount = self._actionCount[self._state][self._actionToExecuteIndex]
        oldReward = self._RTable[self._state][self._actionToExecuteIndex]
        self._RTable[self._state][self._actionToExecuteIndex] = (reward + actionCount * oldReward)/(actionCount + 1)

        # value iteration
        states = self._QTable.keys()

        for state in states :
            possibleActions = self.getPossibleActions(state)

            for actionIndex in possibleActions:
                newState = self.getNextState(state, actionIndex)
                maxValue = max(self._QTable[newState])
                reward = self._RTable[state][actionIndex]
                self._QTable[state][actionIndex] = reward + self._discountFactor * maxValue

        self._state = self.getNextState(self._state, self._actionToExecuteIndex)
        self._actionCount[self._state][self._actionToExecuteIndex] += 1
        #self.printQTable()



    def getReachableStates(self, state):
        actionIndices = self.getPossibleActions(state)
        reachableStates = []

        for actionIndex in actionIndices:
            reachableStates.append( self.getNextState(state, actionIndex))

        return reachableStates

    def getPossibleActions(self, state = None):

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

    def computeActionWeights(self, state, possibleActionIndices):
        penalisationFactor = 10
        possibleActionCounts = [ (penalisationFactor * self._actionCount[state][i] + 1) for i in possibleActionIndices]
        total = sum(possibleActionCounts)
        return [ (total - actionCount) / total for actionCount in possibleActionCounts ]

    def getActionToExecute(self):
        possibleActionsIndexes=self.getPossibleActions()
        if random.random() < self._explorationRate :
            actionWeights = self.computeActionWeights(self._state, possibleActionsIndexes)
            self._actionToExecuteIndex = random.choices(population =possibleActionsIndexes, weights = actionWeights, k = 1)[0]
        else:
            maxIndex=possibleActionsIndexes[0]
            max=self._QTable[self._state][maxIndex]
            for index in possibleActionsIndexes:
                if self._QTable[self._state][index]>max:
                    max = self._QTable[self._state][index]
                    maxIndex=index
            self._actionToExecuteIndex = maxIndex

        return self._actions[self._actionToExecuteIndex]


    def reset(self):
        self._state=self._initialState


