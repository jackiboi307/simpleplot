from simpleplot import *

def f(x):
    return x ** 2

plotter = Plotter()
plotter.init_graphics()

while info := plotter.step():
    if info.moved:
        plotter.draw_func(f)
        plotter.refresh()

