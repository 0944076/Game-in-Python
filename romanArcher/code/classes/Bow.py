from .Arrow import Arrow


class Bow:
    def __init__(self, pygame, screen, asset, x, y):
        self.isAlive = True
        self.screen = screen
        self.width = self.screen[0]*0.02
        self.height = self.screen[1]*0.05
        self.posX = x
        self.posY = y
        self.center = {
            'x': x+self.width/2,
            'y': y+self.height/2
        }
        self.pygame = pygame
        self.asset = asset
        self.object = self.create_object()
        self.drawStart = 0
        self.drawEnd = 0
        self.drawTime = 0

    def update(self):
        if self.drawTime == 0:
            self.width = self.screen[0] * 0.02
            self.height = self.screen[1] * 0.05
            self.set_image('0')
        elif 100 < self.drawTime < 1000:
            self.width = self.screen[0] * 0.05
            self.height = self.screen[1] * 0.05
            self.set_image('1')
        elif 1000 < self.drawTime < 2000:
            self.set_image('2')
        elif 2000 < self.drawTime < 3000:
            self.set_image('3')
        elif self.drawTime >= 3000:
            self.set_image('4')

    def create_object(self):
        img = self.get_image('0')
        rect = img.get_rect()
        rect.x = self.posX
        rect.y = self.posY
        return {
            "item": "bow",
            "type": "image",
            "image": img,
            "rect": rect,
            "layer": "OVERLAY"
        }

    def can_shoot(self, lastShot):
        return lastShot + 1500 < self.pygame.time.get_ticks()

    def shoot(self, mouse, screen_lanes, screen):
        depth = 0

        # Set the depth for the arrow
        wperc = mouse['x']/screen[0]
        lane_height = screen_lanes[1]
        tan5 = 0.08748866352592400522201866943496
        lane_difference = tan5*screen[0]
        adjustement = lane_difference*(1-wperc)
        for x in range(len(screen_lanes)):
            if x == len(screen_lanes) - 1:
                lane_bottom = lane_height + screen_lanes[x]
            else:
                lane_bottom = screen_lanes[x+1]

            if screen_lanes[x]+adjustement < mouse['y'] < lane_bottom+adjustement:
                depth = screen_lanes[x]
                break
        arrowObject = Arrow(self.pygame, self.asset, screen, self.center, mouse, self.drawTime, depth)
        self.drawTime = 0
        return arrowObject

    def check_shot(self, mouse):
        if self.drawStart == 0:
            if mouse['LisActive']:
                self.drawStart = self.pygame.time.get_ticks()
                return False
            else:
                return False
        elif not(mouse['LisActive']):
            self.drawEnd = self.pygame.time.get_ticks()
            self.drawTime = self.drawEnd - self.drawStart
            if self.drawTime > 3000:
                self.drawTime = 3000
            self.drawEnd = self.drawStart = 0
            return True
        else:
            self.drawTime = self.pygame.time.get_ticks() - self.drawStart
            return False

    def get_image(self, sub_img):
        success, img = self.asset.getAsset('bow' + str(sub_img) + '.png')
        if success:
            return img
        else:
            raise ValueError('You ficked up')

    def set_image(self, sort):
        img = self.get_image(sort)
        img = self.pygame.transform.scale(img, (int(self.width), int(self.height)))
        img = self.pygame.transform.rotate(img, 4)
        self.object['image'] = img
