import pyglet
import json
from pyglet.window import mouse
from Game.actors import Tower, Creep, Entity


class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(800, 600)

        #Environment setup
        pyglet.resource.path = ['res', 'res/img', 'res/snd']
        pyglet.resource.reindex()

        #Resources, actors and stuff
        self.config = json.load(open('res/maps/map1/data.json'))

        self.Towers = list()  # Towers in the map
        self.Creeps = list()  # The creeps
        self.AliveCreeps = list()
        self.Cursor = Entity('mouse', 0, 0)
        self.Towers.append(Tower('firebolt', 200, 300))

        for i in range(10):
            self.Creeps.append(Creep('treanth', self.config.path, 1))
        self.creep_cooldown = 3
        self.creep_cooldowntimer = 0

        self.x = 0
        self.y = 0
        self.bgimage = pyglet.resource.image('bg1.png')

    #Events handlers
    def on_draw(self):
        #Clear window
        self.clear()

        #Backgrounds
        self.bgimage.blit(0, 0)
        self.Cursor.render()

        #Towers
        for Tower in self.Towers:
            Tower.render()

            if Tower.dist(self.Cursor) < 200:
                Tower.shoot(self.Cursor)

        #Creeps
        if len(self.AliveCreeps) < len(self.Creeps):
            if time.time() - self.creep_cooldowntimer > self.creep_cooldown:
                self.creep_cooldowntimer = time.time()
                self.AliveCreeps.append(self.Creep[0])

        for Creep in self.AliveCreeps:
            Creep.update()
            Creep.render()

        #GUI

    def on_mouse_motion(self, x, y, dx, dy):
        self.Cursor.x = x
        self.Cursor.y = y

    #Starts
    def game_start(self):
        pyglet.app.run()
