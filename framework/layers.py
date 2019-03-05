class Layer:
    layers = {
        "BACKGROUND"    : [],
        "MIDDLEGROUND"  : [],
        "FOREGROUND"    : [],
        "OVERLAY"       : [],
        "EXTRAOVERLAY"  : [],
        "EXTRAOVERLAY2" : [],
        "EXTRAOVERLAYX" : []

    }
    def __init__(self,surface,pygame):
        self.surface = surface
        self.pygame = pygame
    def setObject(self, layer, object):
        if not layer in self.layers:
            return False
        self.layers[layer].append(object)
        return True
    def draw(self):
        order = ["BACKGROUND","MIDDLEGROUND","FOREGROUND","OVERLAY","EXTRAOVERLAY","EXTRAOVERLAY2","EXTRAOVERLAYX"]
        for layer in order:
            for object in self.layers[layer]:
                if type(object) is dict:
                    if object['type'] == "rect":
                        self.pygame.draw.rect(
                            self.surface,
                            object['color'],
                            object['rect'],
                            object['width']
                        )
                        #rectangle
                    elif object["type"] == "arc":
                        self.pygame.draw.arc(
                            self.surface,
                            object['color'],
                            object['rect'],
                            object['start_angle'],
                            object['stop_angle'],
                            object['width']
                        )
                    elif object["type"] == "line":
                        self.pygame.draw.line(
                            self.surface,
                            object['color'],
                            object['start_pos'],
                            object['end_pos'],
                            object['width']
                        )
                    elif object["type"] == "image":
                        self.surface.blit(object['image'],
                                          object['rect'])
                    if "text" in object:
                        self.surface.blit(object["text"],object["textRect"])
                else:
                    object.draw(self.surface)

    def resetlayer(self, layer):
        if not layer in self.layers:
            return False
        self.layers[layer] = []

    def resetAll(self):
        for layer in self.layers:
            self.resetlayer(layer)
