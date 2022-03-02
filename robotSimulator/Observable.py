class Observable:

    def __init__(self):
        self._observersCallbacks=[]

    def addObserverCallback(self,observerCallback):
        # print(observerCallback)
        self._observersCallbacks.append(observerCallback)

    def deleteObserverCallback(self,observerCallback):
        if observerCallback in self._observersCallbacks:
            self._observersCallbacks.remove(observerCallback)

    def notifyObservers(self):
        for observerCallback in self._observersCallbacks:
            observerCallback(self)

