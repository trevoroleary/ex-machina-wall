from math import pi, tan


def deg_to_rad(deg: float) -> float:
    rad = deg * pi / 180
    return rad % (2 * pi)


def rad_to_deg(rad: float) -> float:
    deg = rad * 180 / pi
    return deg % 360


SCREEN_WIDTH = 900
SCREEN_HEIGH = 500
CIRCLE_RADIUS = 57
X_SPACING = 130
Y_SPACING = X_SPACING * tan(deg_to_rad(30))
FPS = 60
FrameTime = 1/FPS


