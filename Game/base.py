import pyglet
from pyglet.window import mouse


class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(800, 600)

        #Environment setup
        pyglet.resource.path = ['res', 'res/img', 'res/snd']
        pyglet.resource.reindex()

        #Resources, actors and stuff
        self.image = pyglet.resource.image('me.jpg')

    #Events handlers
    def on_draw(self):
        self.clear()
        self.image.blit(0, 0)

    def on_mouse_press(self, x, y, button, modifiers):
        print x, y, button, modifiers

    #Starts
    def game_start(self):
        pyglet.app.run()
