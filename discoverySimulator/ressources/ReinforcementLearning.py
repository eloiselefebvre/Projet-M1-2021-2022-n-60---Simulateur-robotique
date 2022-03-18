import random


class ReinforcementLearning:

    def __init__(self,state):
        self._QTable={}
        self._minimalSpeed = 0
        self._maximalSpeed = 600
        self._numberOfInterval = 2
        self._step = int((self._maximalSpeed - self._minimalSpeed) / self._numberOfInterval)
        self.fillQTable()
        self._learningFactor = 0.1
        self._discountFactor = 0.5
        self._state = state
        self._initialState = state
        self._explorationRate=0.01
        self._actions = [(self._step,0),(-self._step,0),(0,self._step),(0,-self._step),(0,0)]

    # MSO : cadeau - sera utile pour Value Iteration
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

    # MSO TODO : utiliser getNextState() pour calculer le nouvelle Q-Valeur et passer à l'état suivant
    def executedActionFeedback(self,reward):
        self._QTable[self._state][self._actionToExecuteIndex] = (1 - self._learningFactor) * self._QTable[self._state][self._actionToExecuteIndex] + self._learningFactor * reward
        self._state=(self._actions[self._actionToExecuteIndex][0]+self._state[0],self._actions[self._actionToExecuteIndex][1]+self._state[1])

    # MSO : cadeau - j'ai un peu modifié votre fonction pour qu'elle donne les actions possibles dans un état spécifié et pas nécessairement dans l'état courant. Par défaut, l'état courant est utilisé (pour être rétrocompatible)
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

    def getActionToExecute(self):
        possibleActionsIndexes=self.getPossibleActions()
        if random.random() < self._explorationRate or self._QTable[self._state]==[0,0,0,0,0]:       # MSO TODO : la deuxième condition est inutile
            self._actionToExecuteIndex = random.choice(possibleActionsIndexes)
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


