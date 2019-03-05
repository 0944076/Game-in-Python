#I am gonna make a script to manage assets
import os
class AssetManager:
    currentMinigame = "DinoJumper"
    def __init__(self, name,pygame):
        self.pygame = pygame
        self.changeMinigame(name)
    def getAsset(self, name):
         
        path = os.path.join("minigames" ,self.currentMinigame ,"assets")
        if not os.path.isdir(path):
            
            return False,"noDirectory"
            
        path = os.path.join(path, name)
        if not os.path.exists(path):
            return False, "notExists"
        return True, self.pygame.image.load(path)
    def getMusic(self,name):
        path = os.path.join("minigames",self.currentMinigame,"assets")
        if not os.path.isdir(path):
            return False,"noDirectory : " + path 
        path = os.path.join(path, name)
        if not os.path.exists(path):
            return False, "notExists : " + path
        music = self.pygame.mixer.Sound(path)
        return True,music
    def changeMinigame(self, name):
        self.currentMinigame = name
"""  
import pygame
pygame.init()
c = pygame.time.Clock() 
screen=pygame.display.set_mode([800,600])
surface = pygame.display.get_surface()

assets = AssetManager("DinoJumper",pygame)
print(assets.currentMinigame)

success, img = assets.getAsset("Dino.png")
print(success)
if not success:
    print(img)
else:
    
    screen.blit(img,(0,0))
pygame.display.flip() # update the display
c.tick(1000)
"""
