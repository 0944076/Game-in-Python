import importlib
import os
def getGames():
    gameDir = "minigames"
    minionList = {}
    gameList   = {}
    tree = os.listdir("minigames")
    for i in tree:
        path = os.path.join(gameDir,i)
        if os.path.isdir(path) and i != "__pycache__":
            baseImport  = gameDir+"."+i+".code."
            minigame = importlib.import_module(baseImport+"minigame")
            gameList[minigame.name] = minigame.Minigame
            if os.path.isfile(os.path.join(path,"code","minion.py")):
                print("it gets here?")
                minion = importlib.import_module(baseImport+"minion")
                minionList[minion.name] = minion.Minion
    return gameList,minionList
