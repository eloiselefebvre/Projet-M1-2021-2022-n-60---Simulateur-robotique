class Observable:

    TOPICS = ['defaultTopic','selectionChanged','zoomChanged','accelerationChanged','poseChanged','lockChanged']

    def __init__(self):
        self._observersCallbacks={}
        for topic in self.TOPICS:
            self._observersCallbacks[topic]=[]

    def addObserverCallback(self,observerCallback,topic='defaultTopic'):
        if topic in self.TOPICS:
            self._observersCallbacks[topic].append(observerCallback)

    def deleteObserverCallback(self,observerCallback,topic='defaultTopic'):
        if topic in self.TOPICS and observerCallback in self._observersCallbacks[topic]:
            self._observersCallbacks[topic].remove(observerCallback)

    def notifyObservers(self,topic='defaultTopic'):
        for observerCallback in self._observersCallbacks[topic]:
            observerCallback(self)

