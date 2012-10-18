import json
from Game.base import Game


##check events -> window.push_handlers(pyglet.window.event.WindowEventLogger())

#Main entry
if __name__ == '__main__':
    config = json.load(open('config.json'))
    G = Game(config)
    G.game_start()
