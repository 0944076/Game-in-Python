from baseMinions import BaseMinion
name = "Skeleton"
class Minion(BaseMinion):
    def __init__(self):
        BaseMinion.__init__(self)
        self.name = name
        self.minigameName  = "romanArcher"
    def printName(self):
        print(self.name)
