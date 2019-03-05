# button support voor muis

class ButtonAPI:
    allButtons = []
    def __init__(self,pygame):
        self.pygame=pygame
    def create(self,rect,funct):
        self.allButtons.append({"area":rect,"funct":funct})

    def delete(self,index):
        del self.allButtons[index]

    def deleteAll(self):
        self.allButtons=[]

    def updateClicked(self,deltaTime):
        if not self.pygame.mouse.get_pressed()[0]:
            return
        pos=self.pygame.mouse.get_pos()
        for button in self.allButtons:
            if button["area"].collidepoint(pos):
                button["funct"](deltaTime)
                return
