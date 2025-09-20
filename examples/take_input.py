from simpleplot import *
from pygame.locals import *
from math import *

print("press c to update expression")

expr = "x ** 2"
err_occured = False

def f(x):
    global err_occured

    try:
        return eval(expr)

    except Exception as e:
        if not err_occured:
            print(e)
        err_occured = True
        return 0

plotter = Plotter()
plotter.init_graphics()

while info := plotter.step():
    do_update = info.moved 

    for event in info.events:
        if event.type == KEYDOWN:
            if event.key == K_c:
                expr = input("enter expr > ")
                err_occured = False
                do_update = True

    if do_update:
        plotter.draw_func(f)
        plotter.refresh()

