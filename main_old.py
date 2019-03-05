class Player:
  life = 100
  def setLife(self,newLife):
    self.life=newLife
    return self
  def printLife(self):
    print(str(self.name) + " has " + str(self.life))
  def __init__(self,name):
    self.name=name

players = []
def addPlayer(playerName):
  players.append(Player(playerName))
  
addPlayer("lenscas")
addPlayer("awesome")
addPlayer("sucker")

for player in players:
  if player.name=="awesome":
    player.setLife(100).printLife()
  elif player.name=="sucker":
    player.setLife(10).printLife()
  else:
    player.printLife()



