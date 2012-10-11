import pyglet
from pyglet.window import mouse
from Game.actors import Tower, Creep


class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(800, 600)

        #Environment setup
        pyglet.resource.path = ['res', 'res/img', 'res/snd']
        pyglet.resource.reindex()

        #Resources, actors and stuff
        self.Towers = list()  # Towers in the map
        self.Creeps = list()  # The creeps
        self.Towers.append(Tower('firebolt', 200, 300))
        self.Creeps.append(Creep('treanth', 10, 500))

        self.x = 0
        self.y = 0
        self.bgimage = pyglet.resource.image('bg1.png')

    #Methods
    def draw_ent(self, x, y, r=255, g=255, b=255):
        pyglet.graphics.draw(6, pyglet.gl.GL_POLYGON,
            ('v2i', (x - 10, y - 4,
                     x, y - 12,
                     x + 10, y - 4,
                     x + 10, y + 4,
                     x, y + 12,
                     x - 10, y + 4)),
             ('c3B', (
                      r, g, b,
                      r, g, b,
                      r, g, b,
                      r, g, b,
                      r, g, b,
                      r, g, b))
        )

    #Events handlers
    def on_draw(self):
        self.clear()
        self.bgimage.blit(0, 0)
        self.draw_ent(self.x, self.y, 200, 200, 240)

        for Tower in self.Towers:
            self.draw_ent(Tower.x, Tower.y, 10, 10, 240)

    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y

    #Starts
    def game_start(self):
        pyglet.app.run()
