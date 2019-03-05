

class Arrow:

    def __init__(self, pygame, asset, screen, start, mouse, drawTime, depth):
        self.pygame = pygame
        self.asset = asset
        self.screen = screen
        self.timestamp = self.pygame.time.get_ticks()
        self.isAlive = True
        self.gravity = self.screen[1]*0.006
        self.mouse = mouse
        self.depth = depth
        self.posX = start['x']
        self.posY = start['y']
        self.width = self.screen[0]*0.02
        self.height = self.screen[1]*0.053
        self.drawTime = drawTime
        self.velX = self.calculate_vel('x')
        print("~~~~~~~~~~~~~ARROW~~~~~~~~~~~~~")  # DEBUG
        print('velX: ' + str(self.velX))  # DEBUG
        self.velY = self.calculate_vel('y')
        print('velY: ' + str(self.velY))  # DEBUG
        print('lane: ' + str(self.depth/(screen[1]/8)))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")  # DEBUG
        self.object = self.create_object()
        self.landed = False
        self.time_landed = 0

    # Update the arrow
    def update(self):
        if not self.landed:
            self.velY += self.gravity
        self.posX += self.velX
        self.posY += self.velY

        # Set decay
        if self.landed:
            self.velX = 0
            self.velY = 0
            self.decay()

        # Set image
        if self.landed:
            self.set_image('down')
        elif self.velY < -10:
            if self.velX > 40:
                self.set_image('straight')
            else:
                self.set_image('up')
        elif 7 >= self.velY >= -7:
            if self.velX < 10:
                self.set_image('down')
            else:
                self.set_image('straight')
        elif self.velY > 10:
            self.set_image('down')

        # Set coordinates
        self.object['rect'].x = self.posX
        self.object['rect'].y = self.posY
        if not self.landed:
            self.isAlive = self.check_landed()

    # Create the object
    def create_object(self):
        sort = "up"
        img = self.get_img(sort)
        img = self.pygame.transform.scale(img, (int(self.width), int(self.height)))
        rect = img.get_rect()
        rect.x = self.posX
        rect.y = self.posY

        return {
            "item": "arrow",
            "type": "image",
            "image": img,
            "rect": rect,
            "layer": "FOREGROUND"
        }

    # Calculate the velocity
    def calculate_vel(self, cord):
        if cord == 'x':
            result = self.mouse['x']/10*self.drawTime/1000
        elif cord == 'y':
            result = (self.mouse['y'] - self.posY)/10-self.screen[1]/20*self.drawTime/1500
        else:
            result = 0
        return result

    def check_landed(self):
        wperc = self.posX / self.screen[0]
        lane_height = self.screen[1]/8
        tan5 = 0.08748866352592400522201866943496
        lane_difference = tan5 * self.screen[0]
        adjustement = lane_difference * (1 - wperc)
        makeup = self.screen[1]/40
        if self.posY > self.screen[1]:
            return False
        elif self.posX > self.screen[0]:
            return False
        elif (self.posY > self.depth+adjustement-makeup + self.screen[1]/8 and self.velY > 0) and self.timestamp < self.pygame.time.get_ticks() + 2000:
            self.landed = True
            self.time_landed = self.pygame.time.get_ticks()
            return True
        else:
            return True

    def get_img(self, sub_img):
        success, img = self.asset.getAsset('arrow_' + sub_img + '.png')
        if success:
            return img
        else:
            raise ValueError('You ficked up')

    def set_image(self, sort):
        img = self.get_img(sort)
        img = self.pygame.transform.scale(img, (int(self.width), int(self.height)))
        # img = self.pygame.transform.rotate(img, 4)
        self.object['image'] = img

    def decay(self):
        if self.time_landed + 3000 < self.pygame.time.get_ticks():
            self.isAlive = False
