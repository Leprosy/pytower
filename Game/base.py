import pyglet
import json
import time
from pyglet.window import mouse, key
from Game.actors import Tower, Creep, Entity


class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(800, 600)

        #Environment setup
        pyglet.resource.path = ['res', 'res/img', 'res/snd']
        pyglet.resource.reindex()

        #Attributes

        #Init map
        self.start_map(1)

    def start_map(self, map=1):
        #Reset elements
        self.Towers = list()  # Towers in the map
        self.Creeps = list()  # The creeps
        self.x = 0
        self.y = 0

        #Init map data
        self.data = json.load(open('res/maps/map%d/data.json' % map))
        self.Towers.append(Tower('firebolt', 200, 300))
        for i in range(10):
            self.Creeps.append(Creep('treanth', self.data['path'], 1))
        self.creep_cooldown = 3
        self.creep_cooldowntimer = 0
        self.creep_released = 0

        self.bgimage = pyglet.resource.image('bg%d.png' % map)

    #Events handlers
    def on_draw(self):
        #Clear window
        self.clear()

        #Backgrounds
        self.bgimage.blit(0, 0)

        #Towers
        for Tower in self.Towers:
            Tower.render()

        #Creeps
        if self.creep_released < len(self.Creeps):
            if time.time() - self.creep_cooldowntimer > self.creep_cooldown:
                self.creep_cooldowntimer = time.time()
                self.Creeps[self.creep_released].alive = True
                self.creep_released += 1

        for Creep in self.Creeps:
            if Creep.alive is True:
                Creep.update()
                Creep.render()
                
                if Tower.dist(Creep) < Tower.range:
                    Tower.shoot(Creep)

        #GUI

    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y

    def on_key_press(self, symbol, mod):
        if symbol == key.SPACE:
            #self.send_next_wave()
            self.start_map(1)

    #Starts
    def game_start(self):
        pyglet.app.run()

