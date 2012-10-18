import pyglet
import json
import time
from pyglet.window import mouse, key
from Game.actors import Tower, Creep


class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(800, 600)

        #Environment setup
        pyglet.resource.path = ['res', 'res/img', 'res/snd']
        pyglet.resource.reindex()

        #Attributes
        self.x = 0
        self.y = 0

        self.wave = 0
        self.lives = 0
        self.gold = 0
        self.inGame = False

        self.mapdata = None

        #Init map
        self.start_map(1)

    def start_map(self, map_num=1):
        #Load map data
        self.mapdata = json.load(open('res/maps/map%d/data.json' % map_num))

        #Set elements
        self.Towers = list()  # Towers in the map
        self.Creeps = list()  # The creeps

        self.wave = 0
        self.lives = 20
        self.gold = 0
        self.creep_cooldowntimer = 0
        self.creep_released = 0
        self.creep_cooldown = self.mapdata['creep_cooldown']
        self.map_image = pyglet.resource.image('bg%d.png' % map_num)

        self.inGame = True

        #Debug tower
        self.Towers.append(Tower('firebolt', 200, 300))

        #GO!
        self.send_wave()

    def send_wave(self):
        if self.wave < len(self.mapdata['waves']):
            #Generate next wave o'Creeps
            #self.Creeps = list()

            for squad in self.mapdata['waves'][self.wave]:
                for creep in squad:
                    for i in range(squad[creep]):
                        self.Creeps.append(Creep(creep, self.mapdata['path']))

            #D'oh
            self.wave += 1

    def update(self, secs):
        #Clear window
        self.clear()

        #Backgrounds
        self.map_image.blit(0, 0)

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
        pyglet.text.Label("Gold : %d - Lives : %d || Wave : %d" %
                          (self.gold, self.lives, self.wave),
                  font_name='Arial',
                  font_size=8,
                  x=10, y=580,
                  anchor_x='left', anchor_y='center').draw()

    #Events handlers
    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y

    def on_key_press(self, symbol, mod):
        if symbol == key.SPACE:
            self.send_wave()
            #self.start_map(1)

    #Starts
    def game_start(self):
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        pyglet.app.run()
