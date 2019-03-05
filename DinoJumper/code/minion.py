from baseMinions import BaseMinion
name = "Dragon"
class Minion(BaseMinion):
    def __init__(self):
        BaseMinion.__init__(self)
        self.name = name
        self.minigameName = "DinoJumper"
    def printName(self):
        print(self.name)
