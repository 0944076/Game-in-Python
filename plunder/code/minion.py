from baseMinions import BaseMinion
name = "Pirate"
class Minion(BaseMinion):
    def __init__(self):
        BaseMinion.__init__(self)
        self.name = name
        self.minigameName = "plunder"
    def printName(self):
        print(self.name)

