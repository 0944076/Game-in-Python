import random


class Enemy:

    def __init__(self, pygame, asset, screen, depth):
        self.isAlive = True
        self.pygame = pygame
        self.asset = asset
        self.screen = screen
        self.velX = -3
        self.velY = 0.012
        self.depth = depth
        print("enemy depth: " + str(self.depth))
        self.height = screen[1]*0.11
        self.width = screen[0]*0.08
        self.posX = screen[0]
        self.posY = self.depth
        self.object = self.create_object()

    def update(self):
        self.posX += self.velX
        self.posY += self.velY
        self.object['rect'].x = self.posX
        self.object['rect'].y = self.posY

    def create_object(self):
        self.set_angle()

        img = self.get_img()
        img = self.pygame.transform.scale(img, (int(self.width), int(self.height)))
        img = self.pygame.transform.rotate(img, 4)
        rect = img.get_rect()
        self.posY -= self.screen[1]/30
        rect.x = self.posX
        rect.y = self.posY
        return {
            "item": "enemy",
            "type": "image",
            "rect": rect,
            "image": img,
            "layer": "MIDDLEGROUND"
        }

    def get_img(self):
        success, img = self.asset.getAsset('enemy.png')
        if success:
            return img
        else:
            raise ValueError('You ficked up')

    def set_angle(self):
        start_point = self.depth
        end_pointY = 0
        playw= self.screen[0] * 0.06
        playx = self.screen[0] / 20
        end_pointX = playw+playx
        tan4 = 0.0699268119
        end_pointY = start_point + tan4*self.screen[0]
        distance = self.screen[0]-end_pointX
        frames_taken = distance/self.velX
        self.velY = (start_point-end_pointY)/frames_taken
