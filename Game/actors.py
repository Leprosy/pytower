

class Entity:
    """
    All entities(such as towers and creeps) have the same 
    properties, like x and y coordinates and stuff like that.
    """
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.xp = 0
        self.level = 1
        self.x = x
        self.y = y

    def render(self, screen):
        pass


class Creep(Entity):
    pass


class Tower(Entity):
    pass
