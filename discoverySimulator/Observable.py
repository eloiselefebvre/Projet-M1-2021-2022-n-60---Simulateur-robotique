class Observable:

    def __init__(self):
        self.__observersCallbacks={}

    def getTopics(self):
        return self.__observersCallbacks.keys()

    def addObserverCallback(self,observerCallback,topic:str='defaultTopic'):
        if topic in self.__observersCallbacks:
            self.__observersCallbacks[topic].append(observerCallback)
        else:
            self.__observersCallbacks[topic]=[observerCallback]

    def deleteObserverCallback(self,observerCallback,topic:str='defaultTopic'):
        if topic in self.__observersCallbacks and observerCallback in self.__observersCallbacks[topic]:
            self.__observersCallbacks[topic].remove(observerCallback)

    def clearObserverCallback(self):
        self.__observersCallbacks.clear()

    def notifyObservers(self,topic:str='defaultTopic'):
        if topic in self.__observersCallbacks:
            for observerCallback in self.__observersCallbacks[topic]:
                observerCallback(self)



