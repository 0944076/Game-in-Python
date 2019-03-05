

class StartButton:
    def __init__(self, pygame, screen):
        self.pygame = pygame
        self.screen = screen
        self.isAlive = True
        self.w = self.screen[0]*0.6
        self.h = self.screen[1]*0.2
        self.x = self.screen[0]/2 - self.w/2
        self.y = self.screen[1]/2 - self.h/2
        self.object = self.create_startButton(self.x, self.y, self.w, self.h)

    # Create the startButton
    def create_startButton(self, x, y, w, h):
        font = self.pygame.font.SysFont(None, int(0.15 * self.screen[1]))
        textsurface = font.render('Start', True, (128, 128, 128))
        return{
            "type": "rect",
            "rect": self.pygame.Rect(x, y, w, h),
            "color": (255, 255, 255),
            "width": 0,
            "layer": "OVERLAY",
            "text": textsurface,
            "textRect": self.pygame.Rect(x+w/8*3, y+h/4, h/2, w/2)
        }

    def update(self):
        pass
