import pygame

import time
from math import *


RED     = (255, 0, 0)
YELLOW  = (255, 255, 0)
GREEN   = (0, 255, 0)
CYAN    = (0, 255, 255)
BLUE    = (0, 0, 255)
MAGENTA = (255, 0, 255)

DEFAULT_COLOR = BLUE

FG_1 = (255, 255, 255)
FG_2 = (127, 127, 127)
FG_3 = (63, 63, 63)

BG = (0, 0, 0)


def frange(start, end, num):
    for i in range(num - 1):
        yield start + (end - start) / (num - 1) * i

    yield end


class Plotter:
    def __init__(self):
        self.scale = 20
        self.mid = (0, 0)


    def init_graphics(self, default_size=(500, 500)):
        self.screen_size = default_size
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

        pygame.font.init()
        self.font_size = 20
        self.font = pygame.font.Font(size=self.font_size)

        self.mouse_scroll_scale = 0.1
        # self.mouse_move_scale = 0.1
        self.orig_mouse = None
        self.orig_mid = None


    def running(self):
        crosshair_size = 5
        pygame.draw.line(self.screen, FG_3,
            (self.screen_size[0] // 2 - crosshair_size, self.screen_size[1] // 2),
            (self.screen_size[0] // 2 + crosshair_size, self.screen_size[1] // 2))
        pygame.draw.line(self.screen, FG_3,
            (self.screen_size[0] // 2, self.screen_size[1] // 2 - crosshair_size),
            (self.screen_size[0] // 2, self.screen_size[1] // 2 + crosshair_size))

        pygame.display.flip()
        time.sleep(1/60)

        # the above stuff should really happen in the end of the game loop

        self.screen.fill(BG)

        self.draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEWHEEL:
                self.scale = self.scale * (1 + event.y * self.mouse_scroll_scale)
                # plot_ui.scale = max(int(1 / mouse_scroll_scale), min(1000, plot_ui.scale))
                # plot_ui.scale = max(0.1, plot_ui.scale)
                # plot_ui.scale += -0.1 if event.flipped else 0.1
                # print(plot_ui.scale)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.orig_mouse = event.pos
                self.orig_mid = self.mid

            elif event.type == pygame.VIDEORESIZE:
                self.screen_size = self.screen.get_size()

        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            self.mid = (
                self.orig_mid[0] + (self.orig_mouse[0] - mx)
                    * self.scale / self.screen_size[0],
                self.orig_mid[1] - (self.orig_mouse[1] - my)
                    * self.scale / self.screen_size[1]
            )

        return True


    @property
    def x_mid(self):
        return self.mid[0]

    @property
    def y_mid(self):
        return self.mid[1]

    @property
    def x_min(self):
        return self.x_mid - self.scale / 2

    @property
    def x_max(self):
        return self.x_mid + self.scale / 2

    @property
    def y_min(self):
        return self.y_mid - self.scale / 2

    @property
    def y_max(self):
        return self.y_mid + self.scale / 2


    def pos_of(self, pos):
        try:
            # return (
            #     screen_size[0] // 2 - self.x_mid + pos[0] * screen_size[0] / self.x_amount,
            #     screen_size[1] // 2 - self.y_mid - pos[1] * screen_size[1] / self.y_amount
            # )

            x, y = pos

            return (
                (x - self.x_min) / abs(self.x_min - self.x_max) * self.screen_size[0],
                self.screen_size[1] - (y - self.y_min) /
                    abs(self.y_min - self.y_max) * self.screen_size[1],
            )

        except ZeroDivisionError:
            return (0, 0)


    def draw_grid(self):
        # res = 0

        # def f(gen):
        #     zero = False
        #     for i in gen:
        #         if i == 0:
        #             zero = True
        #         yield i
        #     if not zero:
        #         yield 0

        # for y in f(frange(self.y_min, self.y_max, res)):
            # print(y, end=", ")
            # color = FG_1 if y == 0 else FG_3
            # pygame.draw.line(surface, color,
            #     self.pos_of((self.x_min, y)), self.pos_of((self.x_max, y)))

        # print()

        # for x in f(frange(self.x_min, self.x_max, res)):
        #     color = FG_1 if x == 0 else FG_3
        #     pygame.draw.line(surface, color,
        #         self.pos_of((x, self.y_min)), self.pos_of((x, self.y_max)))

        pygame.draw.line(self.screen, FG_1,
            self.pos_of((self.x_min, 0)), self.pos_of((self.x_max, 0)))
        pygame.draw.line(self.screen, FG_1,
            self.pos_of((0, self.y_min)), self.pos_of((0, self.y_max)))

        for (i, line) in enumerate(f"""
xmin = {self.x_min:.2f}
ymin = {self.y_min:.2f}
xmax = {self.x_max:.2f}
ymax = {self.y_max:.2f}
center:
    x = {self.x_mid}
    y = {self.y_mid}
            """.strip().splitlines()):

            s = self.font.render(line, False, FG_2)
            self.screen.blit(s, (10, 10 + i * 0.7 * self.font_size))


    def draw_point(self, point, color=DEFAULT_COLOR):
        pygame.draw.circle(self.screen, color, self.pos_of(point), 3)


    def draw_func(self, f, color=DEFAULT_COLOR):
        res = 1000
        coords = []

        for x in frange(self.x_min, self.x_max, res):
            try:
                coords.append((x, f(x)))
            except ZeroDivisionError:
                pass

        coords = [self.pos_of(point) for point in coords]

        try:
            pygame.draw.lines(self.screen, color, False, coords)
        except ValueError:
            pass

