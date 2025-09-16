import pygame

import time
from math import *


class Color:
    def __init__(self):
        self.red     = (255, 0, 0)
        self.yellow  = (255, 255, 0)
        self.green   = (0, 255, 0)
        self.cyan    = (0, 255, 255)
        self.blue    = (0, 0, 255)
        self.magenta = (255, 0, 255)

        self.fg_1    = (255, 255, 255)
        self.fg_2    = (127, 127, 127)
        self.fg_3    = (63, 63, 63)

        self.bg      = (0, 0, 0)

        self.default = self.blue

    @classmethod
    def invert_color(self, color):
        return (255 - color[0], 255 - color[1], 255 - color[2])

    def invert(self):
        self.fg_1 = __class__.invert_color(self.fg_1)
        self.fg_2 = __class__.invert_color(self.fg_2)
        self.fg_3 = __class__.invert_color(self.fg_3)
        self.bg   = __class__.invert_color(self.bg)


def default(value, default_value):
    return value if value else default_value


def frange(start, end, res):
    for i in range(res - 1):
        yield start + (end - start) / (res - 1) * i

    yield end


def round_step(x, prec):
    # prec is a value like 10, 1, 0.1
    return int(x / prec) * prec


class StepInfo:
    def __init__(self, /, events, moved):
        self.events = events
        self.moved = moved


class Plotter:
    def __init__(self):
        self.scalex = 20
        self.scaley = 20
        self.mid = (0, 0)
        self.color = Color()
        self.running = True
        self.first = True


    def init_graphics(self, default_size=(500, 500)):
        self.screen_size = default_size
        self.font_size = 20
        self.line_size = 1
        self.point_size = 3

        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

        pygame.font.init()
        self.font = pygame.font.Font(size=self.font_size)

        self.fps = 60
        self.mouse_scroll_scale = 0.1
        # self.mouse_move_scale = 0.1
        self.orig_mouse = None
        self.orig_mid = None


    def step(self):
        events = []
        moved = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            elif event.type == pygame.MOUSEWHEEL:
                moved = True
                self.scalex = self.scalex * (1 + event.y * self.mouse_scroll_scale)
                self.scaley = self.scaley * (1 + event.y * self.mouse_scroll_scale)
                # plot_ui.scale = max(int(1 / mouse_scroll_scale), min(1000, plot_ui.scale))
                # plot_ui.scale = max(0.1, plot_ui.scale)
                # plot_ui.scale += -0.1 if event.flipped else 0.1
                # print(plot_ui.scale)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.orig_mouse = event.pos
                self.orig_mid = self.mid

            elif event.type == pygame.VIDEORESIZE:
                moved = True
                orig = self.screen_size
                self.screen_size = self.screen.get_size()
                self.scalex *= self.screen_size[0] / orig[0]
                self.scaley *= self.screen_size[1] / orig[1]

            else:
                events.append(event)

        if pygame.mouse.get_pressed()[0]:
            moved = True
            mx, my = pygame.mouse.get_pos()
            self.mid = (
                self.orig_mid[0] + (self.orig_mouse[0] - mx)
                    * self.scalex / self.screen_size[0],
                self.orig_mid[1] - (self.orig_mouse[1] - my)
                    * self.scaley / self.screen_size[1]
            )

        self.screen.fill(self.color.bg)

        return StepInfo(events=events, moved=moved)


    def refresh(self):
        self.draw_grid()

        crosshair_size = 5
        pygame.draw.line(self.screen, self.color.fg_3,
            (self.screen_size[0] // 2 - crosshair_size, self.screen_size[1] // 2),
            (self.screen_size[0] // 2 + crosshair_size, self.screen_size[1] // 2))
        pygame.draw.line(self.screen, self.color.fg_3,
            (self.screen_size[0] // 2, self.screen_size[1] // 2 - crosshair_size),
            (self.screen_size[0] // 2, self.screen_size[1] // 2 + crosshair_size))

        pygame.display.flip()

        time.sleep(1/self.fps)


    @property
    def x_mid(self):
        return self.mid[0]

    @property
    def y_mid(self):
        return self.mid[1]

    @property
    def x_min(self):
        return self.x_mid - self.scalex / 2

    @property
    def x_max(self):
        return self.x_mid + self.scalex / 2

    @property
    def y_min(self):
        return self.y_mid - self.scaley / 2

    @property
    def y_max(self):
        return self.y_mid + self.scaley / 2

    @property
    def x_step(self):
        return self.scalex / self.screen_size[0]

    @property
    def y_step(self):
        return self.scaley / self.screen_size[1]


    def pos_of(self, pos):
        try:
            x, y = pos
            x = (x - self.x_min) / abs(self.x_min - self.x_max) * self.screen_size[0]
            y = self.screen_size[1] - (y - self.y_min) / \
                abs(self.y_min - self.y_max) * self.screen_size[1]

            return (x, y) if type(x) is not complex and type(y) is not complex else \
                self.pos_of((0, 0))

        except ZeroDivisionError:
            return self.pos_of((0, 0))


    def draw_x(self, x, color=None):
        color = default(color, self.color.fg_2)
        pygame.draw.line(self.screen, color,
            self.pos_of((x, self.y_min)), self.pos_of((x, self.y_max)))

    def draw_y(self, y, color=None):
        color = default(color, self.color.fg_2)
        pygame.draw.line(self.screen, color,
            self.pos_of((self.x_min, y)), self.pos_of((self.x_max, y)))


    def draw_grid(self):
        try:
            ystep = 10 ** int(log10(self.scaley / 2))
            xstep = 10 ** int(log10(self.scalex / 2))

            for i in range(int(self.scaley // ystep) + 1):
                y = round_step(self.y_min, ystep) + ystep * i
                color = self.color.fg_1 if y == 0 else self.color.fg_3
                pygame.draw.line(self.screen, color,
                    self.pos_of((self.x_min, y)), self.pos_of((self.x_max, y)))

            for i in range(int(self.scalex // xstep) + 1):
                x = round_step(self.x_min, xstep) + xstep * i
                color = self.color.fg_1 if x == 0 else self.color.fg_3
                pygame.draw.line(self.screen, color,
                    self.pos_of((x, self.y_min)), self.pos_of((x, self.y_max)))

        except ValueError:
            pass

        self.draw_x(0, self.color.fg_1)
        self.draw_y(0, self.color.fg_1)

        for (i, line) in enumerate(f"""
xmin, xmax = {self.x_min:.2f}, {self.x_max:.2f}
ymin, ymax = {self.y_min:.2f}, {self.y_max:.2f}
xmid = {self.x_mid}
ymid = {self.y_mid}
            """.strip().splitlines()):

            s = self.font.render(line, False, self.color.fg_2)
            self.screen.blit(s, (10, 10 + i * 0.7 * self.font_size))


    def draw_text(self, text):
        for (i, line) in enumerate(text.strip().splitlines()):
            s = self.font.render(line, False, self.color.fg_2)
            self.screen.blit(s, (10,
                self.screen_size[1] - 10 - (i + 1) * 0.7 * self.font_size))


    def draw_point(self, point, color=None):
        color = default(color, self.color.default)
        pygame.draw.circle(self.screen, color, self.pos_of(point), self.point_size)


    def draw_func(self, f, color=None):
        color = default(color, self.color.default)
        coords = []

        for x in frange(self.x_min, self.x_max, self.screen_size[0]):
            try:
                coords.append((x, f(x)))
            except ZeroDivisionError:
                pass

        coords = [self.pos_of(point) for point in coords]

        try:
            pygame.draw.lines(self.screen, color, False, coords, self.line_size)
        except ValueError:
            pass

