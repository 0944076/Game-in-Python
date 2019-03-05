from baseMiniGame import BaseMinigame
from .startscreen import StartScreen
name="plunder"
#Variables and constants:
L0="BACKGROUND"
L1="MIDDLEGROUND"
L2="FOREGROUND"
L3="OVERLAY"
L4="EXTRAOVERLAY"
L5="EXTRAOVERLAY2"
L6="EXTRAOVERLAYX"
re="rect"
ar="arc"
li="line"
BLACK=(0, 0, 0)
BLUE=(29, 95, 130)
RED=(142, 27, 27)
WHITE=(226, 220, 206)
BROWN=(76, 50, 19)
ORANGE=(204, 82, 12)
GREEN=(55, 204, 69)
SKIN1=(96, 74, 72)
SKIN2= (239, 184, 179)


import random

class Minigame(BaseMinigame):

    def start(self):
        self.layer.layers[L4]=[]
        self.layer.layers[L5] = []
        self.layer.layers[L6] = []

        self.captainColour = SKIN1

        self.isOnStart = True

        self.enemySpawned = False

        self.speed = 2
        self.drag = 1
        self.acceleration = 0.7
        self.maxSpeed = 30

        self.maxVelX = 2
        self.maxVelY = 1

        self.inertiaReduction = 1 / (self.drag + 1)

        self.momentumX = 0
        self.momentumY = 0
        self.currentSpeedX = 0
        self.currentSpeedY = 0

        self.rng1 = 0
        self.rng2 = 0
        self.rng3 = 0

        self.spawnx = 0
        self.spawny = 0
        self.timer = 149
        self.movementTimer = 30
        self.enemies = []
        self.deadEnemies = []
        self.overlap = False
        self.collideTimer = 0
        self.numSpawned = 0

        self.attacked = False
        self.sword2X = 0
        self.sword2Y = 0
        self.swordcentX = 0
        self.swordcentY = 0
        self.attackFrame = 0
        self.directionX = 0
        self.directionY = 0

        self.enemiesKilled = 0
        self.health = 100

        self.captainSet = False
        self.healthBarCentered = False
        self.healthBarUpdated = False
        self.countDown = 0
        self.screen = StartScreen(self.framework)
        self.killUpdated = False
        self.killUpdate1 = False
        self.killUpdate2 = False
        self.killGoal = 12
        self.killLeftCounter = 60

        self.skipLose = False
        self.skipWin = False


        success, self.captainER = self.asset.getAsset("Captain E-Right.png")
        success, self.captainWR = self.asset.getAsset("Captain W-Right.png")
        success, self.captainNR = self.asset.getAsset("Captain N-Right.png")
        success, self.captainSR = self.asset.getAsset("Captain S-Right.png")
        success, self.captainNER = self.asset.getAsset("Captain NE-Right.png")
        success, self.captainNWR = self.asset.getAsset("Captain NW-Right.png")

        success, self.captainEL = self.asset.getAsset("Captain E-Left.png")
        success, self.captainWL = self.asset.getAsset("Captain W-Left.png")
        success, self.captainNL = self.asset.getAsset("Captain N-Left.png")
        success, self.captainSL = self.asset.getAsset("Captain S-Left.png")
        success, self.captainNEL = self.asset.getAsset("Captain NE-Left.png")
        success, self.captainNWL = self.asset.getAsset("Captain NW-Left.png")

        success, self.captainEU = self.asset.getAsset("Captain E-Up.png")
        success, self.captainWU = self.asset.getAsset("Captain W-Up.png")
        success, self.captainNU = self.asset.getAsset("Captain N-Up.png")
        success, self.captainSU = self.asset.getAsset("Captain S-Up.png")
        success, self.captainNEU = self.asset.getAsset("Captain NE-Up.png")
        success, self.captainNWU = self.asset.getAsset("Captain NW-Up.png")

        success, self.captainED = self.asset.getAsset("Captain E-Down.png")
        success, self.captainWD = self.asset.getAsset("Captain W-Down.png")
        success, self.captainND = self.asset.getAsset("Captain N-Down.png")
        success, self.captainSD = self.asset.getAsset("Captain S-Down.png")
        success, self.captainNED = self.asset.getAsset("Captain NE-Down.png")
        success, self.captainNWD = self.asset.getAsset("Captain NW-Down.png")

        success, self.enemy0 = self.asset.getAsset("Enemy0.png")
        success, self.enemy1 = self.asset.getAsset("Enemy1.png")
        success, self.enemy2 = self.asset.getAsset("Enemy2.png")
        success, self.enemy3 = self.asset.getAsset("Enemy3.png")
        success, self.enemy4 = self.asset.getAsset("Enemy4.png")
        success, self.enemy5 = self.asset.getAsset("Enemy5.png")
        success, self.enemy6 = self.asset.getAsset("Enemy6.png")

        success, self.enemy0Dam = self.asset.getAsset("Enemy0Dam.png")
        success, self.enemy1Dam = self.asset.getAsset("Enemy1Dam.png")
        success, self.enemy2Dam = self.asset.getAsset("Enemy2Dam.png")
        success, self.enemy3Dam = self.asset.getAsset("Enemy3Dam.png")
        success, self.enemy4Dam = self.asset.getAsset("Enemy4Dam.png")
        success, self.enemy5Dam = self.asset.getAsset("Enemy5Dam.png")
        success, self.enemy6Dam = self.asset.getAsset("Enemy6Dam.png")

        success, self.attackImage = self.asset.getAsset("Attack.png")

        success, self.dead = self.asset.getAsset("Dead.png")

        self.enemiesTextures = [
            self.enemy0, self.enemy1, self.enemy2, self.enemy3, self.enemy4, self.enemy5, self.enemy6
        ]
        self.enemiesTexturesDam = [
            self.enemy0Dam, self.enemy1Dam, self.enemy2Dam, self.enemy3Dam, self.enemy4Dam, self.enemy5Dam, self.enemy6Dam
        ]

    def update(self,deltaTime):
        deltaTime=deltaTime/1000

        if not self.isOnStart:

            if self.skipLose:
                return True, False
            if self.skipWin:
                return True, True

            self.layer.surface.fill(BLACK)

            font = self.pygame.font.SysFont(None, int(0.06 * self.h))
            if self.enemiesKilled == 0:
                killWrite = font.render("You haven't killed any enemies", True, (0, 0, 0))
                self.killLeft = font.render(str(self.killGoal-self.enemiesKilled) + " to go", True, (0, 0, 0))
            if self.enemiesKilled == 1 and not self.killUpdate1:
                killWrite = font.render("You've killed " + str(self.enemiesKilled) + ' enemy', True, (0, 0, 0))
                self.killLeft = font.render(str(self.killGoal - self.enemiesKilled) + " to go", True, (0, 0, 0))
                self.killUpdate1=True
                self.killUpdated=False
                del (self.layer.layers[L0][1])
            if self.enemiesKilled>1 and not self.killUpdate2:
                killWrite = font.render("You've killed "+str(self.enemiesKilled) + ' enemies', True, (0, 0, 0))
                self.killLeft = font.render(str(self.killGoal - self.enemiesKilled) + " to go", True, (0, 0, 0))
                self.killUpdate2 = True
                self.killUpdated = False
                del (self.layer.layers[L0][1])

            self.killText = self.pygame.Rect(0, 0, 2.6667 * 0.25 * self.h, 0.08 * self.h)
            self.killLeftText = self.pygame.Rect(0, 0, 0.16 * self.h, 0.05 * self.h)


            if not self.killUpdated:
                textsurface = killWrite
                self.textsurface2 = self.killLeft
                self.killText.center = (0.74 * self.w, (0.95 * self.h)-1)
                self.killLeftText.center = (0.5 * self.w, (0.05 * self.h)+1)
                killTextBox = self.pygame.Rect(0, 0, 0, 0)
                self.killLeftTextBox = self.pygame.Rect(0, 0, 0, 0)
                killTextBox.center = (self.killText.centerx - textsurface.get_rect().width / 2,
                                      self.killText.centery - textsurface.get_rect().height / 2)
                self.killLeftTextBox.center = (self.killLeftText.centerx - self.textsurface2.get_rect().width / 2,
                                      self.killLeftText.centery - self.textsurface2.get_rect().height / 2)

                self.layer.setObject(L0, {
                    "type": re,
                    re: self.killText,
                    "color": BLACK,
                    "width": 2,
                    "text": textsurface,
                    "textRect": killTextBox
                })
                self.killUpdated = True

            if self.killLeftCounter > 0:
                self.killLeft = font.render(str(self.killGoal - self.enemiesKilled) + " to go", True, (0, 0, 0))
                self.textsurface2 = self.killLeft
                self.killLeftText.center = (0.5 * self.w, (0.05 * self.h) + 1)
                self.killLeftTextBox = self.pygame.Rect(0, 0, 0, 0)
                self.killLeftTextBox.center = (self.killLeftText.centerx - self.textsurface2.get_rect().width / 2,
                                               self.killLeftText.centery - self.textsurface2.get_rect().height / 2)
                self.layer.setObject(L6, {
                    "type": re,
                    re: self.killLeftText,
                    "color": (0,0,0, 1),
                    "width": 1,
                    "text": self.textsurface2,
                    "textRect": self.killLeftTextBox
                })
                self.killLeftCounter = self.killLeftCounter - 1
            else:
                self.layer.resetlayer(L6)

            if not self.healthBarUpdated:
                if self.healthBarCentered:
                    self.healthBar = self.pygame.Rect(self.healthBar.x, self.healthBar.y, 2.6667 * 0.23 * self.h, 0.08 * self.h)
                    self.healthBarFrame = self.pygame.Rect(self.healthBar.x, self.healthBar.y, 2.6667 * 0.23 * self.h, 0.08 * self.h)
                    self.healthBar.w = self.healthBar.w * self.health / 100
                if not self.healthBarCentered:
                    self.healthBar = self.pygame.Rect(0, 0, 2.6667 * 0.23 * self.h, 0.08 * self.h)
                    self.healthBar.w = self.healthBar.w * self.health / 100
                    self.healthBarFrame = self.pygame.Rect(0, 0, 2.6667 * 0.23 * self.h, 0.08 * self.h)
                    self.healthBar.center = (0.24 * self.w, (0.95 * self.h) - 1)
                    self.healthBarFrame.center = (0.24 * self.w, (0.95 * self.h) - 1)
                    self.healthBarCentered = True

                self.layer.setObject(L4, {
                    "type": re,
                    re: self.healthBar,
                    "color": GREEN,
                    "width": 0,
                })
                self.layer.setObject(L5, {
                    "type": re,
                    re: self.healthBarFrame,
                    "color": BLACK,
                    "width": 2,
                })
                self.healthBarUpdated = True

            if self.health < 1:
                self.layer.resetlayer(L3)
                self.layer.resetlayer(L4)
                self.loseText = self.pygame.Rect(0, 0, 2.6667 * 0.30 * self.h, 0.30 * self.h)
                font = self.pygame.font.SysFont(None, int(0.15 * self.h))
                textsurface = font.render('You lose', True, (0, 0, 0))
                self.loseText.center = (0.5 * self.w, 0.5 * self.h)
                loseTextBox = self.pygame.Rect(0, 0, 0, 0)
                loseTextBox.center = (self.loseText.centerx - textsurface.get_rect().width / 2, self.loseText.centery - textsurface.get_rect().height / 2)
                self.layer.setObject(L0, {
                    "type": re,
                    re: self.loseText,
                    "color": BLACK,
                    "width": 10,
                    "text": textsurface,
                    "textRect": loseTextBox
                })
                self.countDown = self.countDown + 1
                if self.countDown > 90:
                    return True, False

            elif not self.enemiesKilled < self.killGoal:

                for enemy in self.enemies:
                    self.layer.layers[L1][enemy.enemyNumber]['image'] = self.dead
                    if enemy.despawnTimer < 1:
                        self.layer.layers[L1][enemy.enemyNumber]['color'] = (13, 86, 119)
                        self.layer.layers[L1][enemy.enemyNumber]['rect'] = self.pygame.Rect(0, 0, 0, 0)
                        self.enemies.remove(enemy)
                        enemy.despawnTimer = 1
                    else:
                        enemy.despawnTimer = enemy.despawnTimer - 1

                self.winText = self.pygame.Rect(0, 0, 2.6667 * 0.30 * self.h, 0.30 * self.h)
                font = self.pygame.font.SysFont(None, int(0.15 * self.h))
                textsurface = font.render('You win', True, (0, 0, 0))
                self.winText.center = (0.5 * self.w, 0.5 * self.h)
                winTextBox = self.pygame.Rect(0, 0, 0, 0)
                winTextBox.center = (self.winText.centerx - textsurface.get_rect().width / 2,
                                      self.winText.centery - textsurface.get_rect().height / 2)
                self.layer.setObject(L0, {
                    "type": re,
                    re: self.winText,
                    "color": BLACK,
                    "width": 10,
                    "text": textsurface,
                    "textRect": winTextBox
                })
                self.countDown = self.countDown + 1
                if self.countDown > 90:
                    return True, True
            if self.collideTimer>0:
                self.collideTimer -= 1


            self.rng1 = random.random()
            #self.rng2 = random.random()
            #self.rng3 = random.random()
            self.spawnx = random.randrange(int(0.1*self.w), int(0.9*self.w))
            self.spawny = random.randrange(int(0.1*self.h), int(0.9*self.h))
            self.timer = self.timer + 1

            if self.timer > 30 and 0.482<self.rng1<0.518 and self.enemiesKilled<self.killGoal:
                enemy = Enemy(self.pygame,self.enemiesTextures, self.enemiesTexturesDam, self.spawnx, self.spawny, 0.03 * self.h, 0.03 * self.h)
                #enemy.enemyImage = random.randint(0, 5)
                self.layer.setObject(L1, enemy.object)
                self.timer = 0
                self.enemies.append(enemy)
                self.layer.layers[L1][self.numSpawned]['color'] = RED
                self.layer.layers[L1][self.numSpawned]['numspawned'] = self.numSpawned
                if enemy.enemyNumber == 0:
                    enemy.enemyNumber = self.numSpawned
                self.numSpawned = self.numSpawned + 1

            enemySpeedX = self.h * 0.002 * deltaTime * self.speed * (self.maxSpeed / 2)
            enemySpeedY = self.h * 0.001 * deltaTime * self.speed * (self.maxSpeed / 2) * 0.5

            if not self.overlap:
                self.layer.resetlayer(L2)
                if self.health > 0:
                    if not self.captainSet:
                        self.captainImage = self.captainER
                        self.captainSet = True


                    self.captain = self.pygame.Rect((self.captain.x, self.captain.y, 0.05 * self.h, 0.05 * self.h))
                    self.captainRect = self.pygame.Rect((self.captain.x, self.captain.y, 0.06 * self.h, 0.06 * self.h))
                    self.captainRect.center = self.captain.center
                    self.captainImage = self.pygame.transform.scale(self.captainImage,
                                                                    ((int(0.065 * self.h)), int(0.065 * self.h)))

                    self.layer.setObject(L2, {
                    "type": "image",
                    "rect": self.captainRect,
                    "image": self.captainImage
                    })
                    if self.collideTimer % 2 == 0:
                        if self.currentSpeedX > 0:
                            if self.directionY < 0 and self.directionX < 0:
                                self.captainImage = self.captainNWR
                            if self.directionY < 0 and self.directionX > 0:
                                self.captainImage = self.captainNER
                            if self.directionY > -1 and self.directionX < 0:
                                self.captainImage = self.captainWR
                            if self.directionY > -1 and self.directionX > 0:
                                self.captainImage = self.captainER
                            if self.directionY > 0 and self.directionX == 0:
                                self.captainImage = self.captainSR
                            if self.directionY < 0 and self.directionX == 0:
                                self.captainImage = self.captainNR
                            if self.directionX == 0 and self.directionY == 0:
                                self.captainImage = self.captainER

                        if self.currentSpeedX < 0:
                            if self.directionY < 0 and self.directionX < 0:
                                self.captainImage = self.captainNWL
                            if self.directionY < 0 and self.directionX > 0:
                                self.captainImage = self.captainNEL
                            if self.directionY > -1 and self.directionX < 0:
                                self.captainImage = self.captainWL
                            if self.directionY > -1 and self.directionX > 0:
                                self.captainImage = self.captainEL
                            if self.directionY > 0 and self.directionX == 0:
                                self.captainImage = self.captainSL
                            if self.directionY < 0 and self.directionX == 0:
                                self.captainImage = self.captainNL
                            if self.directionX == 0 and self.directionY == 0:
                                self.captainImage = self.captainEL

                        if self.currentSpeedX == 0 and self.currentSpeedY > 0:
                            if self.directionY < 0 and self.directionX < 0:
                                self.captainImage = self.captainNWD
                            if self.directionY < 0 and self.directionX > 0:
                                self.captainImage = self.captainNED
                            if self.directionY > -1 and self.directionX < 0:
                                self.captainImage = self.captainWD
                            if self.directionY > -1 and self.directionX > 0:
                                self.captainImage = self.captainED
                            if self.directionY > 0 and self.directionX == 0:
                                self.captainImage = self.captainSD
                            if self.directionY < 0 and self.directionX == 0:
                                self.captainImage = self.captainND
                            if self.directionX == 0 and self.directionY == 0:
                                self.captainImage = self.captainED

                        if self.currentSpeedX == 0 and self.currentSpeedY < 0:
                            if self.directionY < 0 and self.directionX < 0:
                                self.captainImage = self.captainNWU
                            if self.directionY < 0 and self.directionX > 0:
                                self.captainImage = self.captainNEU
                            if self.directionY > -1 and self.directionX < 0:
                                self.captainImage = self.captainWU
                            if self.directionY > -1 and self.directionX > 0:
                                self.captainImage = self.captainEU
                            if self.directionY > 0 and self.directionX == 0:
                                self.captainImage = self.captainSU
                            if self.directionY < 0 and self.directionX == 0:
                                self.captainImage = self.captainNU
                            if self.directionX == 0 and self.directionY == 0:
                                self.captainImage = self.captainEU

                    else: self.captainImage = self.dead

            for enemy in self.enemies:

                if not enemy.imageSet:
                    enemy.enemyImage = random.randint(0, (len(self.enemiesTextures))-1)
                    self.layer.layers[L1][enemy.enemyNumber]['image'] = enemy.textures[enemy.enemyImage]
                    self.layer.layers[L1][enemy.enemyNumber]['image'] = self.pygame.transform.scale(self.layer.layers[L1][enemy.enemyNumber]['image'],((int(0.04 * self.h)), int(0.04 * self.h)))
                    if enemy.enemyImage == 6:
                        enemy.health = 50
                    enemy.imageSet = True


                if enemy.health < 1:
                    self.layer.layers[L1][enemy.enemyNumber]['image'] = self.dead
                    if enemy.despawnTimer < 1:
                        self.layer.layers[L1][enemy.enemyNumber]['color'] = (13, 86, 119)
                        self.layer.layers[L1][enemy.enemyNumber]['rect'] = self.pygame.Rect(0,0,0,0)
                        self.enemies.remove(enemy)
                        enemy.despawnTimer = 1
                        self.enemiesKilled = self.enemiesKilled + 1
                        self.killUpdate2 = False
                        self.layer.resetlayer(L5)
                        self.killLeft = font.render(str(self.killGoal - self.enemiesKilled) + " to go", True, (0, 0, 0))
                        self.killLeftCounter = 60

                    else:
                        enemy.despawnTimer = enemy.despawnTimer - 1



                dx,dy=(enemy.posX+0.015*self.h)-self.captain.centerx,(enemy.posY+0.015*self.h)-self.captain.centery


                sdx, sdy = (enemy.posX+0.015*self.h) - self.swordcentX, (enemy.posY+0.015*self.h) - self.swordcentY

                if not enemy.enemyImage == 2 and not enemy.health<13:
                    enemy.movementTimer = enemy.movementTimer + 1
                if enemy.enemyImage == 5:
                    enemy.maxVelX, enemy.maxVelY = 5, 2.5




                if enemy.ranmovedX and enemy.movementTimer>=40:
                    enemy.ranmovedX = False

                    if enemy.ranmovedY and enemy.movementTimer >= 40:
                        enemy.ranmovedY = False

                if not enemy.enemyImage == 6:
                    if random.random()<0.01 and (enemy.movementTimer>=40 or (enemy.enemyImage == 4 and enemy.movementTimer>10)):
                        enemy.velX = random.choice([-enemy.maxVelX,enemy.maxVelX])
                        enemy.movementTimer = 0
                        enemy.ranmovedX = True

                    if random.random()<0.01 and (enemy.movementTimer>=40 or (enemy.enemyImage == 4 and enemy.movementTimer>10)):
                        enemy.velY = random.choice([-enemy.maxVelY,enemy.maxVelY])
                        enemy.movementTimer = 0
                        enemy.ranmovedY = True

                    if not enemy.ranmovedX and not enemy.ranmovedY and not (enemy.enemyImage == 4):

                        if dx > 0:
                            enemy.velX -= enemySpeedX
                        if dx < 0:
                            enemy.velX += enemySpeedX
                        if dy > 0:
                            enemy.velY -= enemySpeedY
                        if dy < 0:
                            enemy.velY += enemySpeedY
                else:
                    if dx > 0 and enemy.enemyNumber%2==0:
                        enemy.velX -= enemySpeedX
                        enemy.maxVelY = 0
                    if dx < 0 and enemy.enemyNumber%2==0:
                        enemy.velX += enemySpeedX
                        enemy.maxVelY = 0
                    if dy > 0 and enemy.enemyNumber%2!=0:
                        enemy.velY -= enemySpeedY
                        enemy.maxVelX = 0
                    if dy < 0 and enemy.enemyNumber%2!=0:
                        enemy.velY += enemySpeedY
                        enemy.maxVelX = 0



                if enemy.velY < -enemy.maxVelY:
                    enemy.velY += enemySpeedY*2
                if enemy.velY > enemy.maxVelY:
                    enemy.velY -= enemySpeedY*2
                if enemy.velX < -enemy.maxVelX:
                    enemy.velX += enemySpeedX*2
                if enemy.velX > enemy.maxVelX:
                    enemy.velX -= enemySpeedX*2

                enemy.posX = enemy.posX + enemy.velX
                enemy.object['rect'].x = enemy.posX
                enemy.posY = enemy.posY + enemy.velY
                enemy.object['rect'].y = enemy.posY

                if enemy.posX > (self.w - 1.1*enemy.w):
                    enemy.posX = self.w - 1.1*enemy.w

                if enemy.posX < (0.5 * enemy.w):
                    enemy.posX = 0.5 * enemy.w

                if enemy.posY > (self.h - 1.1*enemy.h):
                    enemy.posY = self.h - 1.1*enemy.h

                if enemy.posY < (0.5 * enemy.w):
                    enemy.posY = 0.5 * enemy.w

                if not self.layer.layers[L1][enemy.enemyNumber]['color'] == (209, 50, 111):
                    if enemy.object['rect'].colliderect(self.captain):

                        if self.collideTimer<1:

                            if self.health > 0:
                                self.layer.resetlayer(L2)
                                self.captainColour = SKIN2
                                self.captain = self.pygame.Rect((self.captain.x, self.captain.y, 0.05 * self.h, 0.05 * self.h))
                                self.layer.setObject(L2, {
                                    "type": re,
                                    re: self.captain,
                                    "color": self.captainColour,
                                    "width": 0,
                                })
                                self.overlap=True

                            if dx > 0:
                                self.momentumX -= self.maxSpeed * 2.5
                            if dx < 0:
                                self.momentumX += self.maxSpeed * 2.5
                            if dy > 0:
                                self.momentumY -= self.maxSpeed * 2.5
                            if dy < 0:
                                self.momentumY += self.maxSpeed * 2.5

                            if self.healthBarUpdated:
                                self.health = self.health - 20
                                self.healthBarUpdated = False
                                self.layer.resetlayer(L4)

                            self.collideTimer = 40

                        else:
                            if dx > 0:
                                self.momentumX -= self.maxSpeed/4
                            if dx < 0:
                                self.momentumX += self.maxSpeed/4
                            if dy > 0:
                                self.momentumY -= self.maxSpeed/4
                            if dy < 0:
                                self.momentumY += self.maxSpeed/4

                    else:
                        self.overlap=False

            if self.attacked and self.health>0:

                self.sword2X = self.captain.centerx + (self.directionX * 0.07 * self.h)
                self.sword2Y = self.captain.centery + (self.directionY * 0.07 * self.h)
                self.swordcentX = self.sword2X
                self.swordcentY = self.sword2Y

                swingsize = 0.08

                self.layer.resetlayer(L3)

                if self.attackFrame < 6:

                    if self.directionX == 0:

                        self.sword1 = self.pygame.Rect((self.sword2X - 0.06 * self.h,
                                                        self.sword2Y - 0.01 * self.h * self.directionY, swingsize * self.h,
                                                        swingsize * self.h))
                        self.layer.setObject(L3, {
                            "type": "image",
                            'image': self.attackImage,
                            re: self.sword1,
                        })

                        self.sword1.centerx = self.sword2X - 0.06 * self.h
                        self.sword1.centery = self.sword2Y - 0.01 * self.h * self.directionY
                    elif self.directionY == 0:

                        self.sword1 = self.pygame.Rect((self.sword2X - 0.01 * self.h * self.directionX,
                                                        self.sword2Y - 0.06 * self.h, swingsize * self.h, swingsize * self.h))
                        self.layer.setObject(L3, {
                            "type": "image",
                            'image': self.attackImage,
                            re: self.sword1,
                        })

                        self.sword1.centerx = self.sword2X - 0.01 * self.h * self.directionX
                        self.sword1.centery = self.sword2Y - 0.06 * self.h

                    elif self.directionX != self.directionY:

                        self.sword1 = self.pygame.Rect(
                            (self.sword2X - 0.07 * self.h, self.sword2Y - 0.07 * self.h, swingsize * self.h, swingsize * self.h))
                        self.layer.setObject(L3, {
                            "type": "image",
                            'image': self.attackImage,
                            re: self.sword1,
                        })

                        self.sword1.centerx = self.sword2X - 0.07 * self.h
                        self.sword1.centery = self.sword2Y - 0.07 * self.h

                    elif self.directionX == self.directionY:
                        self.sword1 = self.pygame.Rect(
                            (self.sword2X + 0.05 * self.h, self.sword2Y - 0.05 * self.h, swingsize * self.h, swingsize * self.h))
                        self.layer.setObject(L3, {
                            "type": "image",
                            'image': self.attackImage,
                            re: self.sword1,
                        })

                        self.sword1.centerx = self.sword2X + 0.05 * self.h
                        self.sword1.centery = self.sword2Y - 0.05 * self.h

                    self.swordcentX, self.swordcentY = self.sword1.center

                    if self.enemies != []:

                        for enemy in self.enemies:

                            if enemy.object['rect'].colliderect(self.sword1):
                                if abs(sdx) < abs(dx):
                                    if sdx > 0:
                                        enemy.velX += self.maxVelX * enemy.hitBy * 0.5
                                    if sdx < 0:
                                        enemy.velX -= self.maxVelX * enemy.hitBy * 0.5
                                else:
                                    if dx > 0:
                                        enemy.velX += self.maxVelX * enemy.hitBy * 0.5
                                    if dx < 0:
                                        enemy.velX -= self.maxVelX * enemy.hitBy * 0.5

                                if abs(sdy) < abs(dy):
                                    if sdy > 0:
                                        enemy.velY += self.maxVelY * enemy.hitBy * 0.5
                                    if sdy < 0:
                                        enemy.velY -= self.maxVelY * enemy.hitBy * 0.5
                                else:
                                    if dx > 0:
                                        enemy.velX += self.maxVelX * enemy.hitBy * 0.5
                                    if dx < 0:
                                        enemy.velX -= self.maxVelX * enemy.hitBy * 0.5
                                enemy.health = enemy.health - 1
                                enemy.hitBy = enemy.hitBy + 1
                                self.layer.layers[L1][enemy.enemyNumber]['image'] = enemy.texturesDam[enemy.enemyImage]
                                self.layer.layers[L1][enemy.enemyNumber]['image'] = self.pygame.transform.scale(
                                    self.layer.layers[L1][enemy.enemyNumber]['image'],
                                    ((int(0.04 * self.h)), int(0.04 * self.h)))
                            else:
                                self.layer.layers[L1][enemy.enemyNumber]['image'] = enemy.textures[enemy.enemyImage]
                                self.layer.layers[L1][enemy.enemyNumber]['image'] = self.pygame.transform.scale(
                                    self.layer.layers[L1][enemy.enemyNumber]['image'],
                                    ((int(0.04 * self.h)), int(0.04 * self.h)))



                elif self.attackFrame < 11:

                    self.sword2 = self.pygame.Rect((self.sword2X, self.sword2Y, swingsize * self.h, swingsize * self.h))
                    self.layer.setObject(L3, {
                        "type": "image",
                        'image': self.attackImage,
                        re: self.sword2,
                    })

                    self.sword2.centerx = self.sword2X
                    self.sword2.centery = self.sword2Y

                    self.swordcentX, self.swordcentY = self.sword2.center

                    for enemy in self.enemies:

                        if enemy.object['rect'].colliderect(self.sword2):
                            if abs(sdx) < abs(dx):
                                if sdx > 0:
                                    enemy.velX += self.maxVelX * enemy.hitBy * 0.5
                                if sdx < 0:
                                    enemy.velX -= self.maxVelX * enemy.hitBy * 0.5

                            else:
                                if dx > 0:
                                    enemy.velX += self.maxVelX * enemy.hitBy * 0.5
                                if dx < 0:
                                    enemy.velX -= self.maxVelX * enemy.hitBy * 0.5

                            if abs(sdy) < abs(dy):
                                if sdy > 0:
                                    enemy.velY += self.maxVelY * enemy.hitBy * 0.5
                                if sdy < 0:
                                    enemy.velY -= self.maxVelY * enemy.hitBy * 0.5

                            else:
                                if dx > 0:
                                    enemy.velX += self.maxVelX * enemy.hitBy
                                if dx < 0:
                                    enemy.velX -= self.maxVelX * enemy.hitBy

                            enemy.health = enemy.health - 1
                            enemy.hitBy = enemy.hitBy + 1
                            self.layer.layers[L1][enemy.enemyNumber]['image'] = enemy.texturesDam[enemy.enemyImage]
                            self.layer.layers[L1][enemy.enemyNumber]['image'] = self.pygame.transform.scale(
                                self.layer.layers[L1][enemy.enemyNumber]['image'],
                                ((int(0.04 * self.h)), int(0.04 * self.h)))
                        else:
                            self.layer.layers[L1][enemy.enemyNumber]['image'] = enemy.textures[enemy.enemyImage]
                            self.layer.layers[L1][enemy.enemyNumber]['image'] = self.pygame.transform.scale(
                                self.layer.layers[L1][enemy.enemyNumber]['image'],
                                ((int(0.04 * self.h)), int(0.04 * self.h)))


                elif self.attackFrame < 17:

                    if self.directionX == 0:

                        self.sword3 = self.pygame.Rect((self.sword2X + 0.06 * self.h,
                                                        self.sword2Y - 0.01 * self.h * self.directionY, swingsize * self.h,
                                                        swingsize * self.h))
                        self.layer.setObject(L3, {
                            "type": "image",
                            'image': self.attackImage,
                            re: self.sword3,
                        })

                        self.sword3.centerx = self.sword2X + 0.06 * self.h
                        self.sword3.centery = self.sword2Y - 0.01 * self.h * self.directionY

                    elif self.directionY == 0:

                        self.sword3 = self.pygame.Rect((self.sword2X - 0.01 * self.h * self.directionX,
                                                        self.sword2Y + 0.06 * self.h, swingsize * self.h, swingsize * self.h))
                        self.layer.setObject(L3, {
                            "type": "image",
                            'image': self.attackImage,
                            re: self.sword3,
                        })

                        self.sword3.centerx = self.sword2X - 0.01 * self.h * self.directionX
                        self.sword3.centery = self.sword2Y + 0.06 * self.h

                    elif self.directionX != self.directionY:

                        self.sword3 = self.pygame.Rect(
                            (self.sword2X + 0.07 * self.h, self.sword2Y + 0.07 * self.h, swingsize * self.h, swingsize * self.h))
                        self.layer.setObject(L3, {
                            "type": "image",
                            'image': self.attackImage,
                            re: self.sword3,
                        })

                        self.sword3.centerx = self.sword2X + 0.07 * self.h
                        self.sword3.centery = self.sword2Y + 0.07 * self.h

                    elif self.directionX == self.directionY:
                        self.sword3 = self.pygame.Rect(
                            (self.sword2X - 0.05 * self.h, self.sword2Y + 0.05 * self.h, swingsize * self.h, swingsize * self.h))
                        self.layer.setObject(L3, {
                            "type": "image",
                            'image': self.attackImage,
                            re: self.sword3,
                        })

                        self.sword3.centerx = self.sword2X - 0.05 * self.h
                        self.sword3.centery = self.sword2Y + 0.05 * self.h

                    self.swordcentX, self.swordcentY = self.sword3.center

                    for enemy in self.enemies:

                        if enemy.object['rect'].colliderect(self.sword3):
                            if abs(sdx) < abs(dx):
                                if sdx > 0:
                                    enemy.velX += self.maxVelX * enemy.hitBy * 0.5
                                if sdx < 0:
                                    enemy.velX -= self.maxVelX * enemy.hitBy * 0.5

                            else:
                                if dx > 0:
                                    enemy.velX += self.maxVelX * enemy.hitBy * 0.5
                                if dx < 0:
                                    enemy.velX -= self.maxVelX * enemy.hitBy * 0.5

                            if abs(sdy) < abs(dy):
                                if sdy > 0:
                                    enemy.velY += self.maxVelY * enemy.hitBy * 0.5
                                if sdy < 0:
                                    enemy.velY -= self.maxVelY * enemy.hitBy * 0.5

                            else:
                                if dx > 0:
                                    enemy.velX += self.maxVelX * enemy.hitBy * 0.5
                                if dx < 0:
                                    enemy.velX -= self.maxVelX * enemy.hitBy * 0.5

                            enemy.health = enemy.health - 1
                            enemy.hitBy = enemy.hitBy + 1
                            self.layer.layers[L1][enemy.enemyNumber]['image'] = enemy.texturesDam[enemy.enemyImage]
                            self.layer.layers[L1][enemy.enemyNumber]['image'] = self.pygame.transform.scale(
                                self.layer.layers[L1][enemy.enemyNumber]['image'],
                                ((int(0.04 * self.h)), int(0.04 * self.h)))
                        else:
                            self.layer.layers[L1][enemy.enemyNumber]['image'] = enemy.textures[enemy.enemyImage]
                            self.layer.layers[L1][enemy.enemyNumber]['image'] = self.pygame.transform.scale(
                                self.layer.layers[L1][enemy.enemyNumber]['image'],
                                ((int(0.04 * self.h)), int(0.04 * self.h)))


                elif self.attackFrame == 17:

                    self.attacked = False
                    self.attackFrame = 0
                    self.layer.resetlayer(L3)

                    for enemy in self.enemies:
                        if self.layer.layers[L1][enemy.enemyNumber]['color'] == ORANGE:
                            self.layer.layers[L1][enemy.enemyNumber]['color'] = RED
                        enemy.hitBy = 0

                if self.attackFrame < 17:

                    self.attackFrame = self.attackFrame + 1

            if self.moveX != 0 or self.moveY != 0:
                self.currentSpeedX = (self.moveX+self.momentumX) * self.h * 0.0033 * deltaTime
                self.currentSpeedY = (self.moveY+self.momentumY) * self.h * 0.0033 * deltaTime
                self.captain.x = self.captain.x + self.speed * self.currentSpeedX
                self.captain.y = self.captain.y + self.speed * self.currentSpeedY * 0.5

                if self.moveX > 0 and self.momentumX<self.maxSpeed:
                    self.momentumX = self.momentumX+(0.01+self.acceleration*40*deltaTime)

                if self.moveX < 0 and self.momentumX>-self.maxSpeed:
                    self.momentumX = self.momentumX-(0.01+self.acceleration*40*deltaTime)

                if self.moveY > 0 and self.momentumY<self.maxSpeed:
                    self.momentumY = self.momentumY+(0.01+self.acceleration*40*deltaTime)

                if self.moveY < 0 and self.momentumY>-self.maxSpeed:
                    self.momentumY = self.momentumY-(0.01+self.acceleration*40*deltaTime)

                if self.moveX == 0 and self.momentumX>0:
                    self.momentumX = self.momentumX-(0.01+self.inertiaReduction*10*deltaTime*(abs(self.momentumX/1.8)))
                if self.moveX == 0 and self.momentumX<0:
                    self.momentumX = self.momentumX+(0.01+self.inertiaReduction*10*deltaTime*(abs(self.momentumX/1.8)))
                if self.moveY == 0 and self.momentumY>0:
                    self.momentumY = self.momentumY-(0.01+self.inertiaReduction*10*deltaTime*(abs(self.momentumY/1.8)))
                if self.moveY == 0 and self.momentumY<0:
                    self.momentumY = self.momentumY+(0.01+self.inertiaReduction*10*deltaTime*(abs(self.momentumY/1.8)))



            elif self.moveX == 0 and self.moveY == 0:

                self.captain.x = self.captain.x + self.speed * (self.moveX + self.momentumX) * self.h* 0.00011
                self.captain.y = self.captain.y + self.speed * (self.moveY + self.momentumY) * self.h* 0.00011


                if self.momentumX>0:
                    self.momentumX = self.momentumX-(0.01+self.inertiaReduction*10*deltaTime*(abs(self.momentumX/1.7)))
                if self.momentumX<0:
                    self.momentumX = self.momentumX+(0.01+self.inertiaReduction*10*deltaTime*(abs(self.momentumX/1.7)))
                if self.momentumY>0:
                    self.momentumY = self.momentumY-(0.01+self.inertiaReduction*10*deltaTime*(abs(self.momentumY/1.7)))
                if self.momentumY<0:
                    self.momentumY = self.momentumY+(0.01+self.inertiaReduction*10*deltaTime*(abs(self.momentumY/1.7)))
                if 0 < self.momentumY < 0.5 or 0 > self.momentumY > - 1:
                    self.momentumY = 0
                if 0 < self.momentumX < 0.5 or 0 > self.momentumX > - 1:
                    self.momentumX = 0

            if self.captain.centerx > (self.w - 0.5 * self.captain.w) or self.captain.centerx < (0.5 * self.captain.w):
                self.momentumX = -self.momentumX

            if self.captain.centery > (self.h - 0.5 * self.captain.h) or self.captain.centery < (0.5 * self.captain.h):
                self.momentumY = -self.momentumY

        if self.screen.update(deltaTime) and self.isOnStart:
            #Switch from start to minigame
            self.isOnStart=False
            print("Have fun!")
            self.button.deleteAll()
            self.layer.resetAll()
            self.layer.surface.fill(BLACK)
            success, self.ocean = self.asset.getAsset("Ocean.png")
            self.w, self.h = self.pygame.display.get_surface().get_size()
            if self.w>self.h*1.34:
                self.w=self.h*1.34
            self.ocean = self.pygame.transform.scale(self.ocean, (int((4 / 3) * self.h), int(self.h+(self.h/6))))
            self.layer.setObject(L0, {
                "type": "image",
                "rect": self.ocean.get_rect(),
                "image": self.ocean
            })

            enemy = Enemy(self.pygame, self.enemiesTextures, self.enemiesTexturesDam, self.spawnx, self.spawny, 0.03 * self.h, 0.03 * self.h)
            self.layer.setObject(L1, enemy.object)
            self.timer = 0
            self.enemies.append(enemy)
            self.layer.layers[L1][self.numSpawned]['color'] = RED
            self.layer.layers[L1][self.numSpawned]['numspawned'] = self.numSpawned
            if enemy.enemyNumber == 0:
                enemy.enemyNumber = self.numSpawned
            self.numSpawned = self.numSpawned + 1

            if self.numSpawned > 0:
                self.spawnx = random.randrange(int(0.1 * self.w), int(0.9 * self.w))
                self.spawny = random.randrange(int(0.1 * self.w), int(0.9 * self.h))
                enemy = Enemy(self.pygame, self.enemiesTextures, self.enemiesTexturesDam, self.spawnx, self.spawny, 0.03 * self.h, 0.03 * self.h)
                self.layer.setObject(L1, enemy.object)
                self.timer = 0
                self.enemies.append(enemy)
                self.layer.layers[L1][self.numSpawned]['color'] = RED
                self.layer.layers[L1][self.numSpawned]['numspawned'] = self.numSpawned
                if enemy.enemyNumber == 0:
                    enemy.enemyNumber = self.numSpawned
                self.numSpawned = self.numSpawned + 1

            if self.numSpawned > 1:
                self.spawnx = random.randrange(int(0.1 * self.w), int(0.9 * self.w))
                self.spawny = random.randrange(int(0.1 * self.w), int(0.9 * self.h))
                enemy = Enemy(self.pygame, self.enemiesTextures, self.enemiesTexturesDam, self.spawnx, self.spawny, 0.03 * self.h, 0.03 * self.h)
                self.layer.setObject(L1, enemy.object)
                self.timer = 0
                self.enemies.append(enemy)
                self.layer.layers[L1][self.numSpawned]['color'] = RED
                self.layer.layers[L1][self.numSpawned]['numspawned'] = self.numSpawned
                if enemy.enemyNumber == 0:
                    enemy.enemyNumber = self.numSpawned
                self.numSpawned = self.numSpawned + 1

            if self.numSpawned > 2:
                self.spawnx = random.randrange(int(0.1 * self.w), int(0.9 * self.w))
                self.spawny = random.randrange(int(0.1 * self.w), int(0.9 * self.h))
                enemy = Enemy(self.pygame, self.enemiesTextures, self.enemiesTexturesDam, self.spawnx, self.spawny, 0.03 * self.h, 0.03 * self.h)
                self.layer.setObject(L1, enemy.object)
                self.timer = 0
                self.enemies.append(enemy)
                self.layer.layers[L1][self.numSpawned]['color'] = RED
                self.layer.layers[L1][self.numSpawned]['numspawned'] = self.numSpawned
                if enemy.enemyNumber == 0:
                    enemy.enemyNumber = self.numSpawned
                self.numSpawned = self.numSpawned + 1

            if self.numSpawned > 3:
                self.spawnx = random.randrange(int(0.1 * self.w), int(0.9 * self.w))
                self.spawny = random.randrange(int(0.1 * self.w), int(0.9 * self.h))
                enemy = Enemy(self.pygame, self.enemiesTextures, self.enemiesTexturesDam, self.spawnx, self.spawny, 0.03 * self.h, 0.03 * self.h)
                self.layer.setObject(L1, enemy.object)
                self.timer = 0
                self.enemies.append(enemy)
                self.layer.layers[L1][self.numSpawned]['color'] = RED
                self.layer.layers[L1][self.numSpawned]['numspawned'] = self.numSpawned
                if enemy.enemyNumber == 0:
                    enemy.enemyNumber = self.numSpawned
                self.numSpawned = self.numSpawned + 1

            if self.numSpawned > 4:
                self.spawnx = random.randrange(int(0.1 * self.w), int(0.9 * self.w))
                self.spawny = random.randrange(int(0.1 * self.w), int(0.9 * self.h))
                enemy = Enemy(self.pygame, self.enemiesTextures, self.enemiesTexturesDam, self.spawnx, self.spawny, 0.03 * self.h, 0.03 * self.h)
                self.layer.setObject(L1, enemy.object)
                self.timer = 0
                self.enemies.append(enemy)
                self.layer.layers[L1][self.numSpawned]['color'] = RED
                self.layer.layers[L1][self.numSpawned]['numspawned'] = self.numSpawned
                if enemy.enemyNumber == 0:
                    enemy.enemyNumber = self.numSpawned
                self.numSpawned = self.numSpawned + 1

        #    self.boat=self.pygame.Rect((0, 0, 0.5142*0.70 * self.h, 0.70 * self.h))
        #   self.layer.setObject(L1, {
        #       "type": re,
        #       re: self.boat,
        #       "color": BROWN,
        #       "width": 0,
        #   })

            if self.health > 0:
                self.captain = self.pygame.Rect((0, 0, 0.05 * self.h, 0.05 * self.h))
                self.layer.setObject(L2, {
                    "type": re,
                    re: self.captain,
                    "color": self.captainColour,
                    "width": 0,


                 })
                self.captain.center =0.5*self.w,0.5*self.h

            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_UP, self.moveUp)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_DOWN, self.moveDown)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_LEFT, self.moveLeft)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_RIGHT, self.moveRight)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_w, self.moveUp)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_s, self.moveDown)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_a, self.moveLeft)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_d, self.moveRight)

            self.event.registerEvent(self.pygame.KEYUP, self.pygame.K_UP, self.moveUp)
            self.event.registerEvent(self.pygame.KEYUP, self.pygame.K_DOWN, self.moveDown)
            self.event.registerEvent(self.pygame.KEYUP, self.pygame.K_LEFT, self.moveLeft)
            self.event.registerEvent(self.pygame.KEYUP, self.pygame.K_RIGHT, self.moveRight)
            self.event.registerEvent(self.pygame.KEYUP, self.pygame.K_w, self.moveUp)
            self.event.registerEvent(self.pygame.KEYUP, self.pygame.K_s, self.moveDown)
            self.event.registerEvent(self.pygame.KEYUP, self.pygame.K_a, self.moveLeft)
            self.event.registerEvent(self.pygame.KEYUP, self.pygame.K_d, self.moveRight)

            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_z, self.attack)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_p, self.attack)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_x, self.attack)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_c, self.attack)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_q, self.attack)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_e, self.attack)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_o, self.attack)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_l, self.attack)
            self.event.registerEvent(self.pygame.KEYDOWN, self.pygame.K_SPACE, self.attack)



    moveX = 0
    moveY = 0

    leftPressed=False
    rightPressed=False
    upPressed=False
    downPressed=False

    attackFrame=0

    def attack(self,deltaTime):
        if not self.attacked:
            if self.directionX == 0 and self.directionY == 0 or (self.moveX!=0 or self.moveY!=0):
                self.directionX = self.moveX
                self.directionY = self.moveY
            if self.directionX != 0 or self.directionY != 0:
                self.attacked = True
        if self.health < 1 and self.countDown>10:
            self.skipLose=True
        elif not self.enemiesKilled < self.killGoal and self.countDown>25:
            self.skipWin=True
    def moveLeft(self,deltaTime):
       if self.leftPressed == False:
           self.moveX = self.moveX-1
           self.leftPressed = True
       else:
            self.moveX = self.moveX+1
            self.leftPressed=False

    def moveRight(self,deltaTime):
        if self.rightPressed == False:
            self.moveX = self.moveX+1
            self.rightPressed = True
        else:
            self.moveX = self.moveX-1
            self.rightPressed = False

    def moveUp(self, deltaTime):
        if self.upPressed == False:
            self.moveY = self.moveY-1
            self.upPressed = True
        else:
            self.moveY = self.moveY+1
            self.upPressed = False

    def moveDown(self, deltaTime):
        if self.downPressed == False:
            self.moveY = self.moveY+1
            self.downPressed = True
        else:
            self.moveY = self.moveY-1
            self.downPressed = False

class Enemy:

    enemyColour = WHITE
    enemyNumber = 0
    despawnTimer = 1
    movementTimer = 30
    pygame = None
    posX = 0
    posY = 0
    velX = 0
    velY = 0
    maxVelX = 3
    maxVelY = 1.5
    w = 0
    h = 0
    object = None
    ranmovedX = False
    ranmovedY = False
    health = 14
    hitBy = 0
    enemyImage = 0
    imageSet = False

    def __init__(self, pygame,textures, texturesDam, x, y, w, h):
        self.pygame = pygame
        self.posX = x
        self.posy = y
        self.w = w
        self.h = h
        self.textures = textures
        self.texturesDam = texturesDam
        self.object = self.create_object()

    def create_object(self):
        return {
            'type': 'image',
            'image': self.textures[self.enemyImage],
            'rect': self.pygame.Rect(self.posX, self.posY, self.w, self.h),
        }