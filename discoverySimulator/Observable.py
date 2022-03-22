class Observable:

    def __init__(self):
        self._observersCallbacks={}

    def getTopics(self):
        return self._observersCallbacks.keys()

    def addObserverCallback(self,observerCallback,topic:str='defaultTopic'):
        if topic in self._observersCallbacks:
            self._observersCallbacks[topic].append(observerCallback)
        else:
            self._observersCallbacks[topic]=[observerCallback]

    def deleteObserverCallback(self,observerCallback,topic:str='defaultTopic'):
        if topic in self._observersCallbacks and observerCallback in self._observersCallbacks[topic]:
            self._observersCallbacks[topic].remove(observerCallback)

    def notifyObservers(self,topic:str='defaultTopic'):
        if topic in self._observersCallbacks:
            for observerCallback in self._observersCallbacks[topic]:
                observerCallback(self)



