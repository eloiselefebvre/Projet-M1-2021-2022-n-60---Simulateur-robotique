class Observable:

    def __init__(self):
        self._observersCallbacks={}

    def addObserverCallback(self,observerCallback,topic='defaultTopic'):
        if topic in self._observersCallbacks:
            self._observersCallbacks[topic].append(observerCallback)
        else:
            self._observersCallbacks[topic]=[observerCallback]

    def deleteObserverCallback(self,observerCallback,topic='defaultTopic'):
        if topic in self._observersCallbacks and observerCallback in self._observersCallbacks[topic]:
            self._observersCallbacks[topic].remove(observerCallback)

    def notifyObservers(self,topic='defaultTopic'):
        if topic in self._observersCallbacks:
            for observerCallback in self._observersCallbacks[topic]:
                observerCallback(self)

    def getTopics(self):
        return self._observersCallbacks.keys()

