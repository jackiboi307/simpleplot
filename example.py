from simpleplot import *


def f(x):
    return x * sin(tan(x ** -1))

def rate_of_change(f):
    return lambda x: f(x) - f(x - 1)


plotter = Plotter()
plotter.init_graphics()

while plotter.running():
    plotter.draw_func(f, RED)
    plotter.draw_func(rate_of_change(f), YELLOW)
    plotter.draw_func(rate_of_change(rate_of_change(f)), GREEN)
    plotter.draw_func(rate_of_change(rate_of_change(rate_of_change(f))), CYAN)

    plotter.draw_point((1, 1))
    plotter.draw_point((2, 2))

