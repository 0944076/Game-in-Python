from baseMiniGame import BaseMinigame
#Variables and constants:
L0="BACKGROUND"
L1="MIDDLEGROUND"
L2="FOREGROUND"
L3="OVERLAY"
re="rect"
ar="arc"
li="line"
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
BLUE=(29, 95, 130)
RED=(142, 27, 27)
WHITE=(226, 220, 206)
BROWN=(76, 50, 19)
SKIN1=(96, 74, 72)
SKIN2= (239, 184, 179)

class StartScreen(BaseMinigame):
    hasStarted=False
    instructionsShown=False
    def start(self):
        self.layer.surface.fill((13, 86, 119))

        self.w0, self.h0 = self.pygame.display.get_surface().get_size()
        self.w1, self.h1 = self.pygame.display.get_surface().get_size()

        if self.w1 > self.h1 * 1.34:
            self.w1 = self.h1 * 1.34
        self.screen = self.pygame.Rect(0, 0, self.w1, self.h1)
        self.screen.center = (self.w0 * 0.5, self. h0 * 0.5)
        self.w = self.screen.right
        self.h = self.screen.bottom



        #self.startButton = self.pygame.Rect(0.1 * self.w, 0.35 * self.h, 0.80 * self.w, 0.30 * self.h)
        self.startButton = self.pygame.Rect(0, 0, 2.6667 * 0.30 * self.h, 0.30 * self.h)
        font = self.pygame.font.SysFont(None, int(0.15 * self.h))
        textsurface = font.render('Start', True, (0, 0, 0))
        self.startButton.center = self.screen.center


        #self.instructionsButton = self.pygame.Rect(0.15 * self.w, 0.75 * self.h, 0.70 * self.w, 0.15 * self.h)
        self.instructionsButton = self.pygame.Rect(0, 0, 5 * 0.15 * self.h, 0.15 * self.h)
        font = self.pygame.font.SysFont(None, int(0.15 * self.h))
        textsurface2 = font.render('Instructions', True, (0, 0, 0))
        self.instructionsButton.center = (self.screen.centerx,self.screen.centery+0.3*self.h0)

        startTextBox=self.pygame.Rect(0,0,0,0)
        instructionsTextBox=self.pygame.Rect(0,0,0,0)
        startTextBox.center = (self.startButton.centerx-textsurface.get_rect().width/2, self.startButton.centery-textsurface.get_rect().height/2)
        instructionsTextBox.center = (self.instructionsButton.centerx-textsurface2.get_rect().width/2, self.instructionsButton.centery-textsurface2.get_rect().height/2)

        self.layer.setObject(L2, {
            "type": re,
            re: self.startButton,
            "color": BROWN,
            "width": 0,
            "text": textsurface,
            "textRect": startTextBox
        })
        self.layer.setObject(L2, {
            "type": re,
            re: self.instructionsButton,
            "color": BROWN,
            "width": 0,
            "text": textsurface2,
            "textRect": instructionsTextBox#self.pygame.Rect(0.19 * self.w, 0.78 * self.h, 0.4 * self.w, 0.30 * self.h)
        })

        self.button.create(self.startButton, self.setStarted)
        self.button.create(self.instructionsButton, self.showInstructions)

    def update(self,deltatTime):
        return self.hasStarted
    def setStarted(self, deltaTime):
        if not self.instructionsShown:
            self.hasStarted = True
            print("The game has started.")
        else:
            self.hideInstructions(deltaTime)
    def showInstructions(self, deltaTime):
        if not self.instructionsShown:
            success, self.instructionsImage = self.asset.getAsset("Instructions.png")
            self.instructionsRect = self.pygame.Rect(0.01*self.w, 0.01*self.h, 0.9*1.34*self.h, 0.9*self.h)
            self.instructionsRect.center=(self.w*0.5, self.h*0.5)
            self.instructionsImage = self.pygame.transform.scale(self.instructionsImage, (int(0.9*1.34*self.h), int(0.9*self.h)))
            self.layer.setObject(L3, {
                "type": "image",
                "rect": self.instructionsRect,
                "image": self.instructionsImage
            })
            self.button.create(self.instructionsRect, self.hideInstructions)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_SPACE, self.hideInstructions)
            self.instructionsShown = True
        else:
            self.hideInstructions(deltaTime)
    def hideInstructions(self, deltaTime):
        if self.instructionsShown:
            self.layer.resetlayer(L3)
            self.layer.surface.fill((13, 86, 119))
            self.instructionsShown = False