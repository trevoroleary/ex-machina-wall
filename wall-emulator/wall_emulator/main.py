import pygame
from pygame.locals import *
from wall_emulator.utils import deg_to_rad
from math import tan, sqrt
from wall_emulator.emulator import WallEmulator


def line_endpoint(start_point: tuple, length: float, angle) -> tuple:
    ratio = tan(deg_to_rad(angle))
    # a2 + b2 = length2
    # a2 + (ratio*a)2 = length2
    # a*a + (ratio*ratio*a*a) = length2
    # a2(1 + ratio2) = length2
    # a = sqrt(length2 / (1 + ratio2)
    x = sqrt((length**2) / (1 + (ratio**2)))
    y = ratio * x
    end_point = (start_point[0] + x, start_point[1] + y)
    return end_point


def draw_line(surface, color, start_point, length, angle):
    pygame.draw.line(
        surface=surface,
        color=color,
        start_pos=start_point,
        end_pos=line_endpoint(start_point=start_point, length=length, angle=angle),
        width=2
    )


def main():
    emulator = WallEmulator()
    emulator.run()


if __name__ == "__main__":
    main()
