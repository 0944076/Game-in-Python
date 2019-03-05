class Event:
    def __init__(self,pygame):
        self.pygame=pygame
        self.reset()

    def registerEvent(self,eventType,eventKey,func):
        if eventType in self.dicked:
            innerdicked=self.dicked[eventType]
            innerdicked [eventKey] = func

    def keyCheck (self,deltaTime):
        for event in self.pygame.event.get():
            if event.type in self.dicked:
                if event.key in self.dicked[event.type]:
                    self.dicked [event.type][event.key](deltaTime)
                for inputField in self.inputFields:
                    inputField.get_event(event)
            # Gives a truth value to main.py indicating whether the player quit or not:
            if event.type==self.pygame.QUIT:
                return True
    def addInputField(self,input):
        self.inputFields.append(input)
    def removeAllInputFields(self):
        self.inputFields = []
    def reset(self):
        self.dicked = {self.pygame.KEYDOWN: {}, self.pygame.KEYUP: {}}
        self.inputFields = []





