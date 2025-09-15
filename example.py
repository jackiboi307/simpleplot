from simpleplot import *


def f(x):
    return x ** 3 * sin(tan(x ** -1))

def rate_of_change(f):
    return lambda x: f(x) - f(x - 1)


plotter = Plotter()
plotter.init_graphics()

color = plotter.color

# change background color
color.bg = (12, 12, 12)

# enable light mode by inverting colors (extremely ugly.)
# color.invert()

while plotter.running():
    plotter.draw_func(f, color.red)
    plotter.draw_func(rate_of_change(f), color.yellow)
    plotter.draw_func(rate_of_change(rate_of_change(f)), color.green)
    plotter.draw_func(rate_of_change(rate_of_change(rate_of_change(f))), color.cyan)

    plotter.draw_point((1, 1))
    plotter.draw_point((2, 2))

    try:
        p = (plotter.x_mid, f(plotter.x_mid))
        plotter.draw_point(p, color.fg_1)
        plotter.draw_text(f"f(xmid) = {p[1]}")
    except ZeroDivisionError:
        pass

