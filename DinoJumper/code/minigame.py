from baseMiniGame import BaseMinigame
import random
name = "DinoJumper"
class Minigame(BaseMinigame):
    dinoMusic = None
    dinoMusicChannel = None
    def addCloud(self,loc):
        success, cloudTexture = self.asset.getAsset("cloud.png")
        if success:
            cloudRect = cloudTexture.get_rect()
            cloudRect.x = loc[0]*self.w#0.8*self.h
            cloudRect.y = loc[1]*self.h#0.1*self.w
            cloud = {
                "type" : "image",
                "rect" : cloudRect,
                "image" : cloudTexture
            }
            self.layer.setObject("BACKGROUND",cloud)
        else:
            print("??")
    def start(self):
        if not self.dinoMusic:
            success,self.dinoMusic = self.asset.getMusic("DangerStorm.ogg")
            if not success:
                print(self.dinoMusic)
        if not self.dinoMusicChannel:
            self.dinoMusicChannel = self.dinoMusic.play(-1)
        else:
            self.dinoMusicChannel.unpause()
        self.w,self.h = self.pygame.display.get_surface().get_size()
        self.hasStarted = False
        self.moveSpeed = 0.4
        self.baseMoveSpeed = 2
        self.moveMent = 0
        self.spawnTime = 100
        self.playTime = 30000
        self.pressedEnd = False
        self.registered = False
        self.hasLost = False
        class MeteorGroup(self.pygame.sprite.Group): 
            life = 3
            def update(self,deltaTime):
                for meteor in self.sprites():
                    isHit = meteor.update(deltaTime)
                    if isHit:
                        self.life = self.life - 1 
                return self.life
        self.successLoadedDine,self.imgDino = self.asset.getAsset("Dino.png")
        self.meteorGroup = MeteorGroup()
        self.layer.setObject("FOREGROUND",self.meteorGroup)
        self.pygame.Surface.fill(self.pygame.display.get_surface(),(69,195,200)) 
        
        self.addCloud((0.72,0.2))
        self.addCloud((0.2,0.2))
        
        self.startRect = self.pygame.Rect(0.3*self.w,0.20*self.h,0.55*self.w,0.10*self.h)
        self.startRect.centerx = self.w //2
        # her I am loading the instruction image 
        succes, img5 = self.asset.getAsset("instructions.png")
        print(succes)
        img5 = self.pygame.transform.scale(img5,(int(0.55*self.w),int(0.25*self.h)))
        instRect = img5.get_rect()
        instRect.y = 0.35*self.h
        instRect.centerx = self.w //2
        print(img5) 
        
        self.layer.setObject("OVERLAY",{
            "type" : "image",
            "rect" : instRect,
            "image" : img5
         })
        font = self.pygame.font.SysFont(None, int(0.15*self.h))
        textsurface = font.render("start", True, (51,51,53))
        textRect = textsurface.get_rect()
        textRect.y = 0.2*self.h
        textRect.centerx = self.w // 2
        # her I am making a text for the start button
        self.layer.setObject("OVERLAY",{
            "type" : "rect",
            "rect" : self.startRect,
            "color" : (255,255,255),
            "width" : 0,
            "text" : textsurface,
            "textRect" : textRect
        })  
        # her I am making a surface for the ground
        self.dino,self.dinoGroup = self.createDino()
        self.layer.setObject("FOREGROUND",self.dinoGroup)
        self.groundRect = self.pygame.Rect(0,0.9*self.h,self.w,self.h)
        self.layer.setObject("FOREGROUND",{
            "type" : "rect",
            "rect" : self.groundRect,
            "color" : (102,55,6),
            "width" : 0
        })
        self.button.create(self.startRect, self.onStart)
    def onStart(self,deltaTime):
        print("Start Game")
        self.layer.resetlayer("OVERLAY")
        self.button.deleteAll()
        self.hasStarted = True
        self.layer.surface.fill((69,195,200))
        self.event.registerEvent(self.pygame.KEYUP,self.pygame.K_UP,self.jump) 
        self.event.registerEvent(self.pygame.KEYDOWN,self.pygame.K_RIGHT,lambda x:self.move(1))
        self.event.registerEvent(self.pygame.KEYUP,self.pygame.K_RIGHT,lambda x:self.move(-1))
        self.event.registerEvent(self.pygame.KEYDOWN,self.pygame.K_LEFT,lambda x:self.move(-1))
        self.event.registerEvent(self.pygame.KEYUP,self.pygame.K_LEFT,lambda x:self.move(1))
        print(self.event.dicked)
    # her I am making a rectangle for the character 
    def createDino(self):
        that = self
        class Dino(self.pygame.sprite.Sprite):
            def __init__(self):
                that.pygame.sprite.Sprite.__init__(self)
                
                success,img = that.asset.getAsset("Dino.png")
                if success:
                    self.image = img
                else:
                    print(that.asset.currentMinigame)
                    print(img)
                    raise ValueError('404: Dino not found')
                self.rect = self.image.get_rect()
                print(self.rect.width)
                print(self.rect.height)
                self.rect.x = 0.4*that.w  
                self.rect.y = 0.7*that.h
                self.image = that.pygame.transform.flip(self.image,True,False)
        
        class DinoGroup(self.pygame.sprite.Group): pass
        dino = Dino()
        dinoGroup = DinoGroup()
        dinoGroup.add(dino)
        return dino,dinoGroup
    
    def move(self,dirr):
        print(dirr)
        self.moveMent += dirr
        print(self.moveMent)    
    def createMeteor(self,loc,dirr,target):
        that = self
        class Meteor(self.pygame.sprite.Sprite):
            def __init__(self):
                that.pygame.sprite.Sprite.__init__(self)
                
                success,img = that.asset.getAsset("meteor.png")
                if success:
                    self.image = img
                else:
                    print(that.asset.currentMinigame)
                    print(img)
                    raise ValueError('404: meteor not found')
                if dirr[0] < 0:
                    self.image = that.pygame.transform.flip(self.image,True,False)
                self.rect = self.image.get_rect()
                self.rect.x = loc[0] 
                self.rect.y = loc[1]
                self.target = target 
            def update(self,deltaTime):
                self.rect.x = self.rect.x - (dirr[0]*deltaTime)
                self.rect.y = self.rect.y + (dirr[1]*deltaTime)
                if self.rect.colliderect(self.target):
                    #print("its a hit!")
                    self.remove(self.groups())
                    return True 
                if self.rect.y > that.h:
                    #print("BE GONE!")
                    self.remove(self.groups()) 
        
        
        self.meteorGroup.add(Meteor())
    
    # make dino go up and down, unless hit ground
    
  

    def jump(self,deltaTime):
        if self.checkOnGround():
            self.moveSpeed = -self.baseMoveSpeed 
    
    def checkOnGround(self):
        return self.dino.rect.colliderect(self.groundRect)
    def makeEndScreen(self,hasWon):
        if not self.registered:
            self.registered = True
            font = self.pygame.font.SysFont(None, int(0.15*self.h))
            textsurface = font.render("Won" if hasWon else "Lost", True, (7,7,7))
            rect = textsurface.get_rect()
            rect.centerx = self.w //2
            rect.y = 0.2*self.h
            # her I am making a text for the start button
            self.layer.setObject("OVERLAY",{
                "type" : "rect",
                "rect" : self.startRect,
                "color" : (255,255,255),
                "width" : 0,
                "text" : textsurface,
                "textRect" : rect #self.pygame.Rect(0.51*self.w, 0.185*self.h, 0.4*self.w, 0.10*self.h)
            })
            def shitPython(shit):
                self.pressedEnd = True
            self.button.create(self.startRect,shitPython)
    def update(self, delay):
        
        if not self.hasStarted: return
        self.playTime = self.playTime - delay
        if self.playTime <=0 or self.hasLost:
            self.makeEndScreen(not self.hasLost)
            if self.pressedEnd:
                self.dinoMusicChannel.pause()
                return True,not self.hasLost
            return

        self.layer.surface.fill((69,195,200))
        self.dino.rect.x +=(self.moveMent/5)*delay
        newLife = self.meteorGroup.update(delay)
        self.layer.resetlayer("OVERLAY")
        startX = 0.01
        for life in range(newLife):
            lifeRect= self.pygame.Rect(startX*self.w,0.9*self.h,0.05*self.w,0.02*self.h)
            lifePicture = {
                "type" : "rect",
                "color" : (255,0,0),
                "width" :0,
                "rect" : lifeRect
            }
            self.imgDino = self.pygame.transform.scale(self.imgDino,(int(0.08*self.w),int(0.1*self.h)))
            lifeRect = self.imgDino.get_rect()
            lifeRect.x = startX*self.w
            lifeRect.y = 0.9*self.h
            if self.successLoadedDine:
                lifePicture["type"] = "image"
                lifePicture["image"] = self.imgDino
            self.layer.setObject("OVERLAY",lifePicture)
            startX =startX + 0.08
        if newLife<=0:
            print("you are dead")
            self.hasLost = True
            return
        self.spawnTime = self.spawnTime - delay
        if self.spawnTime<=0:
            self.spawnTime = random.randint(555,645) + self.spawnTime
            changeX = bool(random.randint(0,1))
            changeY = not changeX
            loc     = (self.w*1.1,-(self.h*0.2))
            if changeX:
                loc = (random.randint(-self.w,self.w*2) ,loc[1])
                if loc[0] < 0 or loc[0] > self.w:
                    loc = loc[0],random.randint(-(self.h),self.h*0.5)    
            else:
                loc = loc[0],random.randint(-(self.h),self.h*0.5)
            dirr = random.uniform(-0.5,0.5),random.uniform(0.2,0.8)
            
            self.createMeteor(loc,dirr,self.dino)
        if self.checkOnGround() and self.moveSpeed > 0:
            return                         
        
        self.dino.rect.y = self.dino.rect.y +((self.moveSpeed/delay*self.h))
        if self.checkOnGround():
            self.dino.rect.bottom = 0.92*self.h
            print(self.dino.rect.y)
        self.moveSpeed=self.moveSpeed + (3 * (delay/1000)) 
        



