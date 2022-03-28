import random
from typing import List

class RL:

    DEFAULT_LEARNING_FACTOR = 0.1
    DEFAULT_DISCOUNT_FACTOR = 0.5
    DEFAULT_EXPLORATION_RATE_DECREASE_FACTOR = 0.995

    # Available algorithm : QLearning
    def __init__(self, actionSpaceBuilders:List[dict]=None, stateSpaceBuilders:List[dict]=None, factors:dict=None, QTable:dict=None):
        # TODO : Test validité des entrées & vérification possibilité d'utilisation ValueItération en fonction de si l'état est défini par les actions uniquement
        self.__actionSpaceBuilders=actionSpaceBuilders
        for actionBuilder in self.__actionSpaceBuilders:
            actionBuilder["step"]=round((actionBuilder["max"]-actionBuilder["min"])/actionBuilder["intervals"])

        self.__actions=self.getActionsSpace()

        self.__stateSpaceBuilders=stateSpaceBuilders
        for stateSpaceBuilders in self.__stateSpaceBuilders:
            for actionSpaceBuilders in self.__actionSpaceBuilders:
                if stateSpaceBuilders["id"]==actionSpaceBuilders["id"]:
                    stateSpaceBuilders.update(actionSpaceBuilders)

            if not "step" in stateSpaceBuilders:
                stateSpaceBuilders["step"] = round((stateSpaceBuilders["max"] - stateSpaceBuilders["min"]) / stateSpaceBuilders["intervals"])

        self.__state = self.getState()

        self._QTable=QTable
        self.__explorationRate=0
        if self._QTable is None or not self.isValidTable("_QTable"):
            self._QTable={}
            self.fillTable("_QTable")
            self.__explorationRate = 1

        self._actionCountTable={}
        self.fillTable("_actionCountTable")
        print(self.__actions)

        if factors is None:
            factors = {}
        self.__factors = {
            'learning': RL.DEFAULT_LEARNING_FACTOR,
            'discount': RL.DEFAULT_DISCOUNT_FACTOR,
            'explorationRateDecrease': RL.DEFAULT_EXPLORATION_RATE_DECREASE_FACTOR
        }
        self.__factors.update(factors)


    def isValidTable(self,tableName:str):
        table = self.__getattribute__(tableName)
        if not set(table.keys())==set(self.getStatesSpace()):
            return False
        for state,actions in table.items():
            if len(actions)!=len(self.__actions):
                return False
        return True


    def fillTable(self,tableName:str,initValue:float=0):
        table = self.__getattribute__(tableName)
        for state in self.getStatesSpace():
            table[state]=[initValue] * len(self.__actions)

    def printTable(self,tableName:str):
        table=self.__getattribute__(tableName)
        print(f"----------{tableName}----------")
        for state in table:
            print(state,table[state])
        print("--------------------------------")

    def findCurrent(self, stateSpaceBuilder):
        current = stateSpaceBuilder["getter"]()
        currentMapped = stateSpaceBuilder["min"]
        while currentMapped+stateSpaceBuilder["step"]<=current:
            currentMapped+=stateSpaceBuilder['step']
        return currentMapped

    def getState(self):
        state=[]
        for stateSpaceBuilder in self.__stateSpaceBuilders:
            state.append(self.findCurrent(stateSpaceBuilder))
        return tuple(state)

    def getActionsSpace(self):
        actionSpace=[]
        for actionBuilder in self.__actionSpaceBuilders:
            actionSpace=self.__computeCombinations(actionSpace,[v for v in range(-actionBuilder["step"],2*actionBuilder["step"],actionBuilder["step"])])
        actionSpace = [tuple(action) for action in actionSpace]
        return actionSpace

    def getStatesSpace(self):
        stateSpace=[]
        for stateBuilder in self.__stateSpaceBuilders:
            stateSpace=self.__computeCombinations(stateSpace,[v for v in range(stateBuilder["min"],stateBuilder["max"]+stateBuilder["step"],stateBuilder["step"])])
        stateSpace=[tuple(state) for state in stateSpace]
        return stateSpace

    def __computeCombinations(self,space,value):
        updatedSpace=[]
        if space:
            for a in space:
                for b in value:
                    na=a.copy()
                    na.append(b)
                    updatedSpace.append(na)
        else:
            for b in value:
                updatedSpace.append([b])
        return updatedSpace

    def getPossibleActions(self) -> List[int]:
        """ This method allows to get the possible actions of the robot
        @param state  State of the robot
        @return  Possible actions
        """
        possibleActionIndexes=[i for i in range(len(self.__actions))]
        for i,action in enumerate(self.__actions):
            for j,actionBuilder in enumerate(self.__actionSpaceBuilders):
                current = actionBuilder["getter"]()
                if current+action[j]<actionBuilder["min"] or current+action[j]>actionBuilder["max"]:
                    possibleActionIndexes.remove(i)
                    break
        return possibleActionIndexes

    def execute(self):
        """ This method allows to get the best action to execute
        @return  The action to execute
        """
        possibleActionsIndexes = self.getPossibleActions()
        if random.random() < self.__explorationRate:
            actionWeights = self.__computeActionWeights(self.__state, possibleActionsIndexes)
            self.__executedActionIndex = random.choices(population=possibleActionsIndexes, weights=actionWeights, k=1)[0]
        else:
            maxIndex = possibleActionsIndexes[0]
            max = self._QTable[self.__state][maxIndex]
            for index in possibleActionsIndexes:
                if self._QTable[self.__state][index] > max:
                    max = self._QTable[self.__state][index]
                    maxIndex = index
            self.__executedActionIndex = maxIndex

        for i,actionBuilder in enumerate(self.__actionSpaceBuilders):
            actionBuilder["setter"](actionBuilder["getter"]()+self.__actions[self.__executedActionIndex][i])
        self._actionCountTable[self.__state][self.__executedActionIndex] += 1

    def __computeActionWeights(self, state: tuple, possibleActionIndexes: List[int]) -> List[float]:
        penalisationFactor = 10
        possibleActionCounts = [(penalisationFactor * self._actionCountTable[state][i] + 1) for i in possibleActionIndexes]
        total = sum(possibleActionCounts)
        return [(total - actionCount) / total for actionCount in possibleActionCounts]

    def learn(self,reward):
        self.__explorationRate *= self.__factors["explorationRateDecrease"]
        self._learnQLearning(reward)
        # self.printTable("_QTable")
        # print("exp:",self.__explorationRate)

    def _learnQLearning(self, reward: float):
        """ This method is used to execute the action chosen and to learn (QLearning)
        @param reward  The reward of the action
        """
        nextState = self.getState()
        maxValue = max(self._QTable[nextState])
        self._QTable[self.__state][self.__executedActionIndex] = (1 - self.__factors["learning"]) * self._QTable[self.__state][self.__executedActionIndex] + self.__factors["learning"] * (reward + self.__factors["discount"] * maxValue)
        self.__state = nextState

    def reset(self):
        self._state=self.getState()