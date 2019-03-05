from abc import ABCMeta, abstractmethod

class BaseMinion:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.speed = 10
        self.minigameName = False
        self.name = False
        self.isAlive = True
        self.location = (0,0)
    def startMinigame(self,framework):
        if not self.minigameName:
            throw("No minigame set for "+str(self.name))
        framework["asset"].changeMinigame(self.minigameName)
        return framework["gameList"][self.minigameName](framework)
    @abstractmethod
    def update(self):pass
