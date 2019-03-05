# Standard minigame Imports
from baseMiniGame import BaseMinigame
import cmath
import random

# Imports for the game
from .classes.Player import Player as Player
from .classes.Enemy import Enemy as Enemy
from .classes.StartButton import StartButton as StartButton

name = "romanArcher"


class Minigame(BaseMinigame):

    # Start in Pygame itself
    def start(self):
        # start up variables
        self.objects = {'entities': [], 'statics': [], 'background': []}
        self.nObjects = []
        self.startButton = None
        self.isRunning = False
        self.player = None
        self.lastShot = 0
        self.pointer = None
        self.last_enemy = 0
        self.game_over = False
        self.game_win = False
        self.wave = 1
        self.screen_lanes = [0, 0, 0, 0, 0, 0, 0, 0]
        self.enemies = [[], [], [], [], [], [], [], []]
        self.background_image = None
        self.fence_image = None
        self.kill_counter = 0
        self.font = None
        self.time_ended = 0

        # Set Font stuff
        self.font = self.pygame.font.SysFont("Arial", 16)

        # Get the screen size
        self.screen = self.pygame.display.get_surface().get_size()

        # Define background image
        succes, img = self.asset.getAsset("background.png")
        if succes:
            self.background_image = img
            self.background_image = self.pygame.transform.scale(self.background_image, (int(self.screen[0]), int(self.screen[1])))
        else:
            raise ValueError("You ficked up")

        # Define the 8 screen_lanes
        minScreen = 0
        maxScreen = self.screen[1]
        step = maxScreen / 8
        for x in range(8):
            self.screen_lanes[x] = int(step * x)

        succes, img = self.asset.getAsset("fence_lane_shifted.png")
        if succes:
            self.fence_image = img
            self.fence_image = self.pygame.transform.scale(self.fence_image, (int(self.screen[0]), int(self.screen_lanes[1]/2)))
        else:
            raise ValueError("You ficked up")



        # Make a startButton

        startButton = StartButton(self.pygame, self.screen)
        self.button.create(startButton.object["rect"], self.start_minigame)
        self.objects["statics"].append(startButton)
        self.pointer = {
            'type': 'arc',
            'redValue': 127,
            'color': (127, 30, 30),
            'rect': self.pygame.Rect(0,0,20,20),
            'start_angle': 0,
            'stop_angle': 360/180*cmath.pi,
            'width': 4
        }
        self.set_layers()

    # Update in Pygame itself
    def update(self, delay):
        if self.isRunning:
            if self.game_over or self.game_win:
                self.objects['entities'].clear()
                self.enemies.clear()
                if self.check_exit():
                    if self.game_over:
                        return True, False
                    elif self.game_win:
                        return True, True
            self.set_enemies()
            self.update_objects()
            self.pointer['rect'].x = self.player.mouse['x']-10
            self.pointer['rect'].y = self.player.mouse['y']-10
            if self.player.mouse['LisActive']:
                self.pointer['redValue'] += 8
                if self.pointer['redValue'] > 255:
                    self.pointer['redValue'] = 255
                self.pointer['color'] = (self.pointer['redValue'], 30, 30)
            else:
                self.pointer['redValue'] = 127
                self.pointer['color'] = (127, 30, 30)
            if self.player.bow.check_shot(self.player.mouse):
                self.objects['entities'].append(self.player.bow.shoot(self.player.mouse, self.screen_lanes, self.screen))

            self.set_layers()

    # Start the minigame
    def start_minigame(self, dTime):
        self.button.deleteAll()
        self.objects["statics"].clear()
        self.player = Player(self.pygame, self.screen, self.asset)
        self.isRunning = True

    # Render the objects on the screen
    def set_layers(self):
        self.layer.surface.fill((237, 200, 121))
        self.layer.surface.blit(self.background_image, self.background_image.get_rect())
        self.layer.resetAll()

        # Display the enemies and the lanes
        layer = 0
        for enemyLayer in self.enemies:
            x = 0
            y = self.screen_lanes[layer] - self.fence_image.get_height() / 2
            self.layer.surface.blit(self.pygame.transform.rotate(self.fence_image, 5), (int(x), int(y)))
            for enemy in enemyLayer:
                self.layer.surface.blit(enemy.object['image'], enemy.object['rect'])
            layer += 1

        # Put all the other entities in the layers
        # Render the arrows
        for o in self.objects['entities']:
            if o.isAlive:
                self.layer.setObject(o.object["layer"], o.object)
        for o in self.objects['statics']:
            if o.isAlive:
                self.layer.setObject(o.object["layer"], o.object)

        # Set layer for the player
        if self.player:
            self.layer.surface.blit(self.player.object["image"], self.player.object['rect'])
            self.layer.surface.blit(self.player.bow.object["image"], self.player.bow.object['rect'])

            # Set the cursor
            self.pygame.draw.arc(self.layer.surface, self.pointer['color'], self.pointer['rect'],
                                 self.pointer['start_angle'], self.pointer['stop_angle'], self.pointer['width'])

            # Set the wave
            self.layer.surface.blit(self.font.render("wave: " + str(self.wave), 1, (0, 0, 0)), (0, 0))

        if self.game_win or self.game_over:
            w = self.screen[0]*0.5
            h = self.screen[1]*0.3
            textSize = (int(w), int(h))
            if self.game_win:
                winImage = self.pygame.transform.scale(self.player.object["image"],
                                                        (int(self.screen[0]*(1/3)), int(self.screen[1]*0.2)))
                winImage = self.pygame.transform.rotate(winImage, -4)
                text = self.font.render("You shot all the enemies", 1, (0, 0, 0))
                text = self.pygame.transform.scale(text, textSize)

                self.layer.surface.blit(text, (self.screen[0]/2 - textSize[0]/2, self.screen[1]/2 - textSize[1]/2))
                self.layer.surface.blit(winImage, (self.screen[0] / 2 - winImage.get_width()/2, self.screen[1]/2 + textSize[1]/2))
            if self.game_over:
                deadImage = self.pygame.transform.scale(self.player.object["image"],
                                                        (int(self.screen[0]*(1/3)), int(self.screen[1]*0.4)))
                deadImage = self.pygame.transform.rotate(deadImage, 90)
                text = self.font.render("You lost a life", 1, (0, 0, 0))
                text = self.pygame.transform.scale(text, textSize)
                self.layer.surface.blit(text, (self.screen[0] / 2 - text.get_width() / 2, self.screen[1] / 2 - text.get_height() / 2))
                self.layer.surface.blit(deadImage, (self.screen[0] / 2 - deadImage.get_width() / 2, self.screen[1] / 2 + textSize[1] / 2))

    # Update all the objects in the list
    def update_objects(self):
        if self.player:
            self.player.update()

        j = 0
        for enemyLayer in self.enemies:
            i=0
            for enemy in enemyLayer:
                if enemy.isAlive:
                    if self.check_gameover(enemy):
                        self.game_over = True
                    enemy.update()
                else:
                    self.enemies[j].pop(i)
                i += 1
            j += 1

        for objectList in self.objects:
            i = 0
            for o in self.objects[objectList]:
                if o.isAlive:
                    if objectList == "entities":
                        # Check for arrow collision
                        if o.object['item'] == 'arrow':
                            for enemyLayer in self.enemies:
                                for enemy in enemyLayer:
                                    if o.object['rect'].colliderect(enemy.object['rect']) and o.depth == enemy.depth:
                                        o.isAlive = False
                                        enemy.isAlive = False
                                        self.kill_counter += 1
                                        if self.kill_counter == 4 and self.wave == 1:
                                            self.wave += 1
                                        if self.kill_counter == 10 and self.wave == 2:
                                            self.wave += 1
                                        if self.kill_counter == 21 and self.wave == 3:
                                            self.game_win = True
                                            self.time_ended = self.pygame.time.get_ticks()
                                            print("You won")

                    if o.isAlive:
                        o.update()
                    else:
                        self.objects[objectList].pop(i)
                        print("popping", i)
                else:
                    self.objects[objectList].pop(i)
                    print("popping", i)
                i += 1

    def set_enemies(self):
        if not(self.game_win or self.game_over):
            ticks = self.pygame.time.get_ticks()
            if self.last_enemy + 6000/self.wave < ticks:
                minScreen = int(0)
                maxScreen = int(self.screen[1])
                step = int(maxScreen / 8)
                depth = random.randrange(minScreen, maxScreen-self.screen_lanes[1], step)
                new_enemy = Enemy(self.pygame, self.asset, self.screen, depth)
                nDepth = depth//step
                self.enemies[nDepth].append(new_enemy)
                self.last_enemy = ticks

    def check_gameover(self, enemy):
        if self.player:
            if enemy.object['rect'].x < self.player.object['rect'].x + self.player.object['rect'].width:
                self.time_ended = self.pygame.time.get_ticks()
                return True
            else:
                return False

    def check_exit(self):
        if self.time_ended + 4000 < self.pygame.time.get_ticks():
            if self.game_win:
                return True
            elif self.game_over:
                return True
            else:
                return False

        else:
            return False
