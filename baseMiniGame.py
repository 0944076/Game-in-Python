from abc import ABCMeta, abstractmethod

class BaseMinigame:
    def __init__(self,framework):
        self.framework  = framework
        self.gameList   = framework["gameList"]
        self.minionList = framework["minionList"]
        self.pygame     = framework["pygame"]
        self.asset      = framework["asset"]
        self.button     = framework["button"]
        self.layer      = framework["layer"]
        self.event      = framework["event"]
        self.counter    = 0
        self.start()

    def start(self): pass
    @abstractmethod

    def update(self,deltaTime): pass
