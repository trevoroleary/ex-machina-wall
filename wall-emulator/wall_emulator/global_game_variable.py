from wall_emulator.utils import deg_to_rad
from math import tan


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Global:

    def __init__(self):
        self._x_spacing = 130
        self.x_spacing_adjust = 0
        self._circle_radius = 57
        self.circle_radius_adjust = 0

    @property
    def y_spacing(self):
        return self.x_spacing * tan(deg_to_rad(30))

    @property
    def x_spacing(self):
        return self._x_spacing + self.x_spacing_adjust

    @property
    def circle_radius(self):
        return self._circle_radius + self.circle_radius_adjust

    @property
    def fps(self):
        return 60
