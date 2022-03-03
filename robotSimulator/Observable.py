class Observable:

    TOPICS = ['selectionChanged','zoomChanged','accelerationChanged','poseChanged']

    def __init__(self):
        self._observersCallbacks={}
        for topic in self.TOPICS:
            self._observersCallbacks[topic]=[]

    def addObserverCallback(self,observerCallback,topic):
        if topic in self.TOPICS:
            self._observersCallbacks[topic].append(observerCallback)

    def deleteObserverCallback(self,observerCallback,topic):
        if topic in self.TOPICS and observerCallback in self._observersCallbacks[topic]:
            self._observersCallbacks[topic].remove(observerCallback)

    def notifyObservers(self,topic):
        for observerCallback in self._observersCallbacks[topic]:
            observerCallback(self)

