
from time import perf_counter_ns
from typing import Iterable
from neopixel import NeoPixel
from enums import COLORS, ColorGenerator

class Segment:
    def __init__(self, pixels: NeoPixel, start_position: int, end_position: int, glasses_left: bool = False, glasses_right: bool = False):
        self.pixels = pixels
        self.num_pixels = end_position - start_position
        self.start_position = start_position
        self.end_position = end_position
        self.glasses_left = glasses_left
        self.glasses_right = glasses_right
        self.color_generator = ColorGenerator(byte_order=self.pixels.byteorder)
        self.write_offset = 20 if self.glasses_right else 0

    def sync_sweep_right(self, percentage: int, color_on: COLORS, color_off: COLORS, draw: bool = False):
        iter_number = int((self.num_pixels * percentage / 100)) + self.start_position
        self.sweep_right(iter_number=iter_number, color_on=color_on, color_off=color_off, draw=draw)
    
    def sync_sweep_left(self, percentage: int, color_on: COLORS, color_off: COLORS, draw: bool = False):
        iter_number = int((self.num_pixels * percentage / 100)) + self.start_position
        self.sweep_left(iter_number=iter_number, color_on=color_on, color_off=color_off, draw=draw)

    def sweep_right(self, iter_number: int, color_on: COLORS, color_off: COLORS, draw: bool = False):
        color_on = color_on.value[self.pixels.byteorder]
        color_off = color_off.value[self.pixels.byteorder]
        for i in self.forward:
            self.pixels[i] = color_on if i > iter_number else color_off
        if draw:
            self.pixels.show()
    
    def sweep_left(self, iter_number: int, color_on: COLORS, color_off: COLORS, draw: bool = False):
        color_on = color_on.value[self.pixels.byteorder]
        color_off = color_off.value[self.pixels.byteorder]
        iter_number = len(self.pixels) - iter_number
        for i in self.forward:
            self.pixels[i] = color_off if i > iter_number else color_on
        if draw:
            self.pixels.show()
    
    def set_all(self, color: COLORS, draw: bool = False):
        if not isinstance(color, tuple):
            color = color.value[self.pixels.byteorder]
        self.pixels[self.start_position: self.end_position] = [color]*self.num_pixels
        if draw:
            self.pixels.show()
    
    def skip_some(self, iter_number: int, skip_length: int, color_on: COLORS, color_off: COLORS, draw: bool = False):
        color_on = color_on.value[self.pixels.byteorder]
        color_off = color_off.value[self.pixels.byteorder]
        for i in self.forward:
            if (((i + iter_number) % skip_length) + 1) > skip_length/2:
                color = color_on
            else:
                color = color_off
            self.pixels[i] = color
        if draw:
            self.pixels.show()

    def set_time_color(self, multiplier: float = 1, draw: bool = False):
        self.set_all(color=self.color_generator.time_color(multiplier=multiplier), draw=draw)
    
    @property
    def forward(self) -> Iterable:
        if self.glasses_right:
            indexes = list(range(self.start_position + self.write_offset, self.end_position)) + list(range(self.start_position, self.start_position + self.write_offset))
            indexes.reverse()
            return indexes
        return range(self.start_position, self.end_position)

    @property
    def reverse(self) -> Iterable:
        return range(self.end_position -1, self.start_position -1, -1)
    