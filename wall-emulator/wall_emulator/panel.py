from math import tan, sqrt
from random import random
from wall_emulator.utils import deg_to_rad
from wall_emulator.global_game_variable import Global
import pygame
from pygame import BLEND_RGB_ADD


class Led:
    def __init__(self, canvas):
        self.canvas = canvas
        pass

    def draw_led(self, centre: tuple, r, g, b):
        led_surfaces = list()
        number = 25
        for i in range(number):
            surface = pygame.Surface((100, 100))
            surface.set_colorkey((0, 0, 0))
            surface.set_alpha(128)
            pygame.draw.circle(surface, (r/number, g/number, b/number), (50, 50), i*2)
            led_surfaces.append(surface)
        for surface in led_surfaces:
            self.canvas.blit(surface, (centre[0]-50, centre[1]-50), special_flags=BLEND_RGB_ADD)


class Panel:
    def __init__(self, canvas, centre_point: tuple, top: bool, left: bool, right: bool):
        self.canvas = canvas
        self.v = Global()
        self.centre_point = (self.canvas.get_size()[0]*random(), self.canvas.get_size()[1]*random())
        self.centre_point_target = centre_point
        self._x_error_prev = None
        self._y_error_prev = None
        self.leds = [Led(canvas=canvas) for i in range(3)]
        self.top = top
        self.left = left
        self.right = right

    def set_panel_target(self, x, y):
        self.centre_point_target = (x, y)

    def _update_centre_points(self):
        p_gain = 0.07
        d_gain = 0.004
        x, y = self.centre_point
        target_x, target_y = self.centre_point_target
        x_error = x - target_x
        y_error = y - target_y

        if self._y_error_prev is None:
            self._y_error_prev = y_error
            y = y - (y_error * p_gain)
        else:
            d_error_dt = (self._y_error_prev - y_error)*self.v.fps
            y = y - (p_gain*y_error - d_gain*d_error_dt)
            self._y_error_prev = y_error

        if self._x_error_prev is None:
            self._x_error_prev = x_error
            x = x - (x_error*p_gain)
        else:
            d_error_dt = (self._x_error_prev - x_error)*self.v.fps
            x = x - (p_gain*x_error - d_gain*d_error_dt)
            self._x_error_prev = x_error

        self.centre_point = (x, y)

    def draw_panel(self):
        """
        Main three points are at -30, 90 and 210 degrees
        # The other circles are at.. 270, 150, 30
        """
        self._update_centre_points()
        offset = 12

        points = list()
        for degree in range(-30, 330, 1):
            # if degree < -20 or (80<=degree<100) or (200<=degree<220):
            if (-30 + offset) <= degree <= (90 - offset):
                mapping = list(range(270 - offset + 2, 0, -1))
                index = degree + 20
                degree = mapping[index]
                x, y = self._get_x_y_from_deg_and_radius(degree=degree, radius=self.v.circle_radius)
                x = -x + self.v.x_spacing / 2 + self.centre_point[0]
                y = y - (self.v.y_spacing / 2) + self.centre_point[1]
                points.append((x, y))
            elif (90 + offset) <= degree <= (210 - offset):
                mapping = list(range(390 - offset + 2, 0, -1))
                index = degree - 100
                degree = mapping[index]
                x, y = self._get_x_y_from_deg_and_radius(degree=degree, radius=self.v.circle_radius)
                x = x - self.v.x_spacing / 2 + self.centre_point[0]
                y = -y + -self.v.y_spacing / 2 + self.centre_point[1]
                points.append((x, y))
            elif (210 + offset) <= degree <= (330 - offset):
                mapping = list(range(150 - offset + 2, 0, -1))
                index = degree - 220
                degree = mapping[index]
                x, y = self._get_x_y_from_deg_and_radius(degree=degree, radius=self.v.circle_radius)
                if degree > 90:
                    x = -x + self.centre_point[0]
                else:
                    x = x + self.centre_point[0]
                y = -abs(y) + self.v.y_spacing + self.centre_point[1]
                points.append((x, y))
            elif degree < (-30 + offset):
                x, y = self._get_x_y_from_deg_and_radius(degree=degree, radius=self.v.circle_radius)
                x = x + self.centre_point[0]
                y = -y + self.centre_point[1]
                points.append((x, y))
            elif (90 - offset) <= degree < (90 + offset):
                x, y = self._get_x_y_from_deg_and_radius(degree=degree, radius=self.v.circle_radius)
                if 90 < degree:
                    x = -x + self.centre_point[0]
                    y = y + self.centre_point[1]
                else:
                    x = x + self.centre_point[0]
                    y = -y + self.centre_point[1]
                points.append((x, y))
            elif (210 - offset) <= degree < (210 + offset):
                x, y = self._get_x_y_from_deg_and_radius(degree=degree, radius=self.v.circle_radius)
                x = -x + self.centre_point[0]
                y = y + self.centre_point[1]
                points.append((x, y))
            else:
                x, y = self._get_x_y_from_deg_and_radius(degree=degree, radius=self.v.circle_radius)
                x = x + self.centre_point[0]
                y = -y + self.centre_point[1]
                points.append((x, y))
        pygame.draw.polygon(surface=self.canvas, color=pygame.Color("black"), points=points)
        pygame.draw.aalines(surface=self.canvas, color=pygame.Color("black"), closed=True, points=points, blend=100)
        # pygame.draw.circle(surface=canvas, color=RED, center=centre_point, radius=2)
        return points

    def draw_leds(self):
        if self.top:
            led_1 = (self.centre_point[0], self.centre_point[1] - self.v.y_spacing/2)
            self.leds[0].draw_led(centre=led_1, r=100*random(), g=100*random(), b=100*random())
        # sin(angle) = opposite/hypotenuse
        opposite = tan(deg_to_rad(210)) * self.v.circle_radius / 2
        if self.left:
            led_2 = (self.centre_point[0] - opposite, self.centre_point[1] + opposite)
            self.leds[1].draw_led(centre=led_2, r=100*random(), g=100*random(), b=100*random())
        if self.right:
            led_3 = (self.centre_point[0] + opposite, self.centre_point[1] + opposite)
            self.leds[2].draw_led(centre=led_3, r=100*random(), g=100*random(), b=100*random())

    def _get_x_y_from_deg_and_radius(self, degree: float, radius: float) -> tuple:
        ratio = tan(deg_to_rad(degree))
        x = sqrt((radius ** 2) / (1 + (ratio ** 2)))
        y = ratio * x
        return x, y


class Panels:
    def __init__(self, canvas, starting_x: int, starting_y: int):
        self.canvas = canvas
        self.v = Global()
        self.starting_x = starting_x
        self.starting_y = starting_y
        no_top_panels = [1, 5, 9, 13, 17, 19, 23, 27, 31]
        no_left_panels = [3, 4, 8, 12, 16, 17, 18]
        no_right_panels = [4, 8, 12, 15, 16, 31, 32]
        self.panels = [Panel(
            canvas=canvas,
            centre_point=(0, 0),
            top=(i+1) not in no_top_panels,
            left=(i+1) not in no_left_panels,
            right=(i+1) not in no_right_panels
        ) for i in range(32)]
        self.update_positions()
        pass

    def handle_events(self, events):
        pass

    def draw(self, screen_width: int, screen_height: int):
        for panel in self.panels:
            panel.draw_leds()
        for panel in self.panels:
            self.update_positions()
            panel.draw_panel()

    def update_positions(self):
        # Draw grid number 1
        index = 0
        for x in range(4):
            for y in range(4):
                self.panels[index].set_panel_target(
                    x=self.starting_x + (self.v.x_spacing * x),
                    y=self.starting_y + (self.v.y_spacing * y)
                )
                index += 1

        for x in range(5):
            y_range = 2 if x in [0, 4] else 4
            y_offset = self.v.y_spacing if x in [0, 4] else 0
            for y in range(y_range):
                self.panels[index].set_panel_target(
                    x=-self.v.x_spacing + self.starting_x + (self.v.x_spacing / 2) + (self.v.x_spacing * x),
                    y=y_offset + self.starting_y - (self.v.y_spacing / 2) + (self.v.y_spacing * y)
                )
                index += 1


