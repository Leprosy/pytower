import pyglet
from pyglet.window import mouse
from Game import actors

#Define resources
window = pyglet.window.Window(800, 600)
T = actors.Tower("treanth")
sound = pyglet.resource.media('res/snd/shot.wav', streaming=False)
image = pyglet.resource.image('res/img/me.jpg')
label = pyglet.text.Label(T.name,
                          font_name='Times New Roman',
                          font_size=20,
                          x=window.width // 2, y=window.height // 2,
                          anchor_x='center', anchor_y='center')


#Helpers
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


#Events handlers
@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)
    label.draw()

    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 1, 2, 3],
    ('v2i', (100, 100,
             150, 100,
             150, 150,
             100, 150))
    )


@window.event
def on_mouse_press(x, y, button, modifiers):
    sound.play()
    if button == mouse.LEFT:
        print 'The left mouse button was pressed at .', x, ':', y


#check events -> window.push_handlers(pyglet.window.event.WindowEventLogger())
pyglet.app.run()
