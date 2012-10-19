import pyglet
import json
from pyglet.window import mouse, key
from Game.actors import Tower, Creep


class Game(pyglet.window.Window):
    def __init__(self, config):
        super(Game, self).__init__(800, 600, caption=config['title'],
                                   vsync=False)

        #Environment setup
        self.config_data = config
        pyglet.resource.path = [self.config_data['game_res'],
                                self.config_data['game_res'] + '/img',
                                self.config_data['game_res'] + '/snd']
        pyglet.resource.reindex()

        self.set_icon(pyglet.resource.image('icon16.png'),
                      pyglet.resource.image('icon32.png'),
                      pyglet.resource.image('icon64.png'),
                      pyglet.resource.image('icon128.png'))

        #Attributes
        self.x = 0
        self.y = 0
        self.selected_tower = None

        self.wave = 0
        self.lives = 0
        self.gold = 0
        self.inGame = False

        self.mapdata = None

        self.clock = pyglet.clock.ClockDisplay()

        #Init map
        #self.start_map(1)

    def start_map(self, map_num=1):
        #Load map data
        self.mapdata = json.load(open(self.config_data['game_res'] +
                                      '/maps/map%d/data.json' % map_num))

        #Set elements
        self.Towers = list()  # Towers in the map
        self.Creeps = list()  # The creeps

        self.wave = 0
        self.lives = 20
        self.gold = 300
        self.creep_released = 0
        self.creep_cooldown = self.mapdata['creep_cooldown']
        self.map_image = pyglet.resource.image('bg%d.png' % map_num)

        self.inGame = True

        #Debug tower
        self.Towers.append(Tower('firebolt', 200, 300))

    def send_wave(self):
        if self.creep_released < len(self.Creeps):
            return
        if self.wave >= len(self.mapdata['waves']):
            return

        #Generate next wave o'Creeps
        self.creep_released = 0
        self.Creeps = list()

        for squad in self.mapdata['waves'][self.wave]:
            for creep in squad:
                for i in range(squad[creep]):
                    self.Creeps.append(Creep(creep, self.mapdata['path']))

        #D'oh
        self.wave += 1

        #Schedule the sending of the first creep(I hate creeps)
        pyglet.clock.schedule_once(self.send_creep, self.creep_cooldown)

    def send_creep(self, secs):
        #Is there any creep left to release?
        if self.creep_released < len(self.Creeps):
            self.Creeps[self.creep_released].alive = True
            self.creep_released += 1

            #Schedule the next creep
            pyglet.clock.schedule_once(self.send_creep, self.creep_cooldown)

    def update(self, secs):
        #Clear window
        self.clear()

        if self.inGame:
            #Backgrounds
            self.map_image.blit(0, 0)

            #self.update_towers()
            self.update_creeps()

            #GUI
            self.draw_gameGUI()

        else:
            #Main menu
            self.draw_mainmenu()

    def update_creeps(self):
        #Creeps
        for Creep in self.Creeps:
            #Alive and well? move and draw
            if Creep.alive is True:
                Creep.update()
                Creep.render()

                #Lost a life
                if Creep.reached_end:
                    self.lives -= 1
                    self.Creeps.remove(Creep)

                    if self.lives <= 0:
                        self.inGame = False

            #Dead creep => profit
            if Creep.alive is False and Creep.hp <= 0:
                self.gold += self.Creep.gold
                self.Creeps.remove(Creep)

    def draw_gameGUI(self):
            pyglet.text.Label("Gold : %d - Lives : %d" %
                              (self.gold, self.lives),
                              font_name='Arial',
                              font_size=8,
                              x=10, y=580,
                              anchor_x='left', anchor_y='center').draw()
            pyglet.text.Label("Wave : %d - Released : %d" %
                              (self.wave, self.creep_released),
                              font_name='Arial',
                              font_size=8,
                              x=600, y=580,
                              anchor_x='left', anchor_y='center').draw()

            if self.selected_tower is not None:
                pyglet.text.Label("%s selected" %
                                  self.Towers[self.selected_tower].name,
                                  font_name='Arial',
                                  font_size=8,
                                  x=300, y=550,
                                  anchor_x='center', anchor_y='center').draw()

            self.clock.draw()

    def draw_mainmenu(self):
            pyglet.text.Label("Towers R Us",
                              font_name='Arial',
                              font_size=32,
                              x=100, y=300,
                              anchor_x='left', anchor_y='center').draw()
            pyglet.text.Label("< Press Spacebar to start >",
                              font_name='Arial',
                              font_size=14,
                              x=100, y=250,
                              anchor_x='left', anchor_y='center').draw()
            pyglet.text.Label("< Press ESC to exit >",
                              font_name='Arial',
                              font_size=14,
                              x=100, y=230,
                              anchor_x='left', anchor_y='center').draw()

    #Events handlers
    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y

    def on_mouse_press(self, x, y, button, modifiers):
        #In game mouse clicks
        if self.inGame:
            if button == mouse.LEFT:
                i = 0
                selected = False

                #Pick a tower
                for tower in self.Towers:
                    r = tower.radius * 2

                    if x >= tower.x - r and x <= tower.x + r:
                        if y >= tower.y - r and y <= tower.y + r:
                            self.selected_tower = i
                            selected = True
                    i += 1

                if selected is False:
                    self.selected_tower = None

                    if self.gold >= 150:
                        self.Towers.append(Tower('firebolt', x, y))
                        self.gold -= 150

    def on_key_press(self, symbol, mod):
        #Main menu keys
        if self.inGame is False:
            if symbol == key.SPACE:
                self.start_map(1)
            if symbol == key.ESCAPE:
                quit()

        #In game keys
        else:
            if symbol == key.ESCAPE:
                self.inGame = False

            if symbol == key.SPACE:
                self.send_wave()

    #Starts
    def game_start(self):
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        pyglet.app.run()
