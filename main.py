import pyglet
from pyglet.window import mouse
from Game.base import Game


##check events -> window.push_handlers(pyglet.window.event.WindowEventLogger())

#Main entry
if __name__ == '__main__':
    G = Game()
    G.game_start()
