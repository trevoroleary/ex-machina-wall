from enum import Enum
from time import perf_counter
from types import new_class
import random

class SPEED(Enum):
    FASTEST = 0.01
    FASTER = 0.03
    FAST = 0.07
    SLOW = 0.1
    SLOWER = 0.4
    SLOWEST = 0.8

class COLORS(Enum):
    RED = {
        "RGBW": (0, 255, 0, 0),
        "RGB": (0, 255, 0)
    }
    GREEN = {
        "RGBW": (255, 0, 0, 0),
        "RGB": (255, 0, 0)
    }
    BLUE = {
        "RGBW": (0, 0, 255, 0),
        "RGB": (0, 0, 255)
    }
    WHITE = {
        "RGBW": (0, 0, 0, 255),
        "RGB": (255, 255, 255)
    }
    OFF = {
        "RGBW": (0, 0, 0, 0),
        "RGB": (0, 0, 0)
    }

    RED_BLUE = {
        "RGBW": (0, 255, 50, 0),
        "RGB": (0, 255, 50)
    }

    def random_color():
        color = COLORS.OFF
        while color == COLORS.OFF:
            color = random.choice(list(COLORS))
        return color
        

class MODES(Enum):
    NOTHING = 0
    SKIP_SOME = 1
    PULSE = 2
    FLASH = 3
    BUILD = 4

    def succ(self):
        v = self.value + 1
        if v > 4:
            v = 0
        return MODES(v)

class ColorGenerator:
    def __init__(self, byte_order):
        self.start_time = perf_counter()
        self.byte_order = byte_order
    
    def time_color(self, multiplier: float = 1) -> tuple:
        new_time = perf_counter()
        td = (new_time - self.start_time) * multiplier

        color_wheel_position = int(td % 256)
        return self.color_wheel(color_wheel_position)
        
    def color_wheel(self, position):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if position < 0 or position > 255:
            r = g = b = 0
        elif position < 85:
            r = int(position * 3)
            g = int(255 - position * 3)
            b = 0
        elif position < 170:
            position -= 85
            r = int(255 - position * 3)
            g = 0
            b = int(position * 3)
        else:
            position -= 170
            r = 0
            g = int(position * 3)
            b = int(255 - position * 3)
        
        if self.byte_order == "RGBW":
            return (r, g, b, 0)
        return (r, g, b)