from .Bow import Bow
class Player:
    def __init__(self, pygame, screen, asset):
        self.asset = asset
        self.screen = screen
        self.pygame = pygame
        self.isAlive = True
        self.posX = 0
        self.posY = 0
        self.height = 0.
        self.width = 0
        self.object = self.create_object()
        self.bow = None
        self.create_bow()
        self.mouse = {"x": 0,
                      "y": 0,
                      "LisActive": False,
                      "RisActive": False}

    # Update the object
    def update(self):
        self.update_mouse()
        self.bow.update()

    # Create the player object
    def create_object(self):
        self.width = w = self.screen[0] * 0.06
        self.height = h = self.screen[1] * 0.08
        self.posX = self.screen[0]/20
        self.posY = self.screen[1]/2-h/2

        img = self.get_img()
        img = self.pygame.transform.scale(img, (int(self.width), int(self.height)))
        img = self.pygame.transform.rotate(img, 4)
        rect = img.get_rect()
        rect.x = self.posX
        rect.y = self.posY
        return {
            "item": "player",
            "type": "image",
            "rect": rect,
            "image": img,
            "layer": "FOREGROUND"
        }

    def create_bow(self):
        w = self.screen[0]*0.02
        h = self.screen[1]*0.05
        x = self.posX+self.screen[0]*0.03
        y = self.posY + self.height/2-h/2+self.screen[1]*0.02
        self.bow = Bow(self.pygame, self.screen, self.asset, x, y)

    # Update mouse position
    def update_mouse(self):
        mPos = self.pygame.mouse.get_pos()
        mClicked = self.pygame.mouse.get_pressed()
        self.mouse['x'] = mPos[0]
        self.mouse['y'] = mPos[1]
        self.mouse['LisActive'] = mClicked[0]
        self.mouse['RisActive'] = mClicked[2]

    # Retrieve position of coordinates
    def get_coord(self, retrieve=None):
        if type(retrieve) == list:
            result = []
            for asked in retrieve:
                if asked == 'x':
                    result.append(self.posX)
                elif asked == 'y':
                    result.append(self.posY)
                elif asked == 'h':
                    result.append(self.height)
                elif asked == 'w':
                    result.append(self.width)
                elif asked == 'xMax':
                    result.append(self.width + self.posX)
                elif asked == 'yMax':
                    result.append(self.height + self.posY)
            return result
        else:
            return {
                'x': self.posX,
                'y': self.posY,
                'xMax': self.posX + self.width,
                'yMax': self.posY + self.height,
                'h': self.height,
                'w': self.width
            }

    def get_img(self):
        success, img = self.asset.getAsset('archer.png')
        if success:
            return img
        else:
            raise ValueError("You\'re amzing, its not your problem :)")
