class Observable:

    def __init__(self):
        self._observersCallbacks={
            "selectionChanged":[],
            "zoomChanged":[],
            "accelerationChanged":[],
            "poseChanged":[]
        }

    def addObserverCallback(self,observerCallback,topic):
        if topic in self._observersCallbacks:
            self._observersCallbacks[topic].append(observerCallback)

    def deleteObserverCallback(self,observerCallback,topic):
        if topic in self._observersCallbacks and observerCallback in self._observersCallbacks[topic]:
            self._observersCallbacks[topic].remove(observerCallback)

    def notifyObservers(self,topic):
        for observerCallback in self._observersCallbacks[topic]:
            observerCallback(self)

