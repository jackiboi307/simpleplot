from simpleplot import *
from pygame.locals import *


def f(x):
    return x ** 3 * sin(tan(x ** -1))

def rate_of_change(f):
    return lambda x: (f(x) - f(x - dx)) / dx


plotter = Plotter()
plotter.init_graphics()
# plotter.line_size = 2
# plotter.point_size = 5

color = plotter.color

# change background color
color.bg = (12, 12, 12)

# enable light mode by inverting colors (extremely ugly.)
# color.invert()

# incrementation of dx
dx = plotter.x_step
INC_STEP = 0.02
do_inc = True
inv_inc = False


while info := plotter.step():
    # press space to toggle incrementation
    for event in info.events:
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                do_inc = not do_inc
                if do_inc:
                    inv_inc = not inv_inc

    if do_inc:
        dx += INC_STEP if not inv_inc else -INC_STEP

    # do not redraw if nothing has changed
    if info.moved or do_inc:
        plotter.draw_func(f, color.red)
        plotter.draw_func(rate_of_change(f), color.yellow)
        plotter.draw_func(rate_of_change(rate_of_change(f)), color.green)
        plotter.draw_func(rate_of_change(rate_of_change(rate_of_change(f))), color.cyan)

        plotter.draw_point((1, 1))
        plotter.draw_point((2, 2))

        plotter.draw_text("example text")

        plotter.refresh()

