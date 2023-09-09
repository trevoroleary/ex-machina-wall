
from time import perf_counter_ns, sleep
from typing import Iterable
from neopixel import NeoPixel
from enums import COLORS, ColorGenerator
import board
import neopixel
import threading
from enum import Enum
from enums import COLORS, SPEED, ColorGenerator
from behaviour_lists import *
from enums import IntColor

class Eye:
    def __init__(self, pixels: NeoPixel, start_position: int, end_position: int, left: bool = False, right: bool = False):
        self.pixels = pixels
        self.num_pixels = end_position - start_position
        self.start_position = start_position
        self.end_position = end_position
        self.left = left
        self.right = right
        self.color_generator = ColorGenerator(byte_order=self.pixels.byteorder)
        self.write_offset = 20 if self.left else 21
        self.int_color = IntColor(byte_order=self.pixels.byteorder)
        self.colors = [(0,0,0), (0, 0, 0), (0, 0, 0)]
        self.stop = False

    def draw(self):
        self.pixels.show()

    def get_index(self, iter_number: int, shift: int = 0, inv: bool = True) -> int:
        if not inv and self.right:
            additional_offset = -6
        else:
            additional_offset = 0
        index = (iter_number + self.write_offset + additional_offset) % self.num_pixels + shift
        if self.right and inv:
            index = self.num_pixels - index
        if index < 0:
            index += self.num_pixels
        index = index%self.num_pixels
        index = self.start_position + index
        return index

    def color(self, index) -> tuple:
        return self.colors[index]

    def nominal_behaviour(self, iter_number: int, shift: int = 0, draw: bool = False):
        index = self.get_index(iter_number=iter_number, shift=shift)
        self.pixels[index] = self.color(NOMINAL[iter_number%self.num_pixels])
        if draw:
            self.draw()
    
    def draw_animation(self, iter_number: int, animation: list, draw: bool = False):
        for i in range(self.num_pixels):
            if self.stop:
                self.stop = False
                return True
            index = self.get_index(iter_number=i)
            self.pixels[index] = self.color(animation[iter_number][i])
        if draw:
            self.draw()
    
    def draw_individual_animation(self, iter_number, animation: list, draw: bool = False):
        animation = [animation[iter_number][0]] if self.left else [animation[iter_number][1]]
        return self.draw_animation(iter_number=0, animation=animation, draw=draw)
    
    def draw_animation_no_inv(self, iter_number: int, animation: list, draw: bool = False):
        for i in range(self.num_pixels):
            if self.stop:
                self.stop = False
                return True
            index = self.get_index(iter_number=i, inv=False)
            self.pixels[index] = self.color(animation[iter_number][i])
        if draw:
            self.draw()
            
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
    
# pixels_ring = neopixel.NeoPixel(
#             board.D21, 
#             48,
#             brightness=0.1,
#             auto_write=False,
#             pixel_order=neopixel.RGB
#         )
# left_eye = Eye(pixels=pixels_ring, start_position=0, end_position=24, left=True)
# right_eye = Eye(pixels=pixels_ring, start_position=24, end_position=48, right=True)
# left_eye.set_all(color=COLORS.OFF, draw=True)
# right_eye.set_all(color=COLORS.OFF, draw=True)

# for i in range(10):
    # for shift in [0, -1]:
        # for i in range(24):
            # left_eye.nominal_behaviour(iter_number=i, shift=shift, draw=False)
            # right_eye.nominal_behaviour(iter_number=i, shift=shift, draw=False)
        # right_eye.draw()
        # sleep(SPEED.SLOW.value)

def play_animation(animat):
    for i in range(len(animat)):
        left_eye.draw_animation(iter_number=i, animation=animat, draw=False)
        right_eye.draw_animation(iter_number=i, animation=animat, draw=False)
        right_eye.draw()
        sleep(SPEED.FAST.value)

def play_non_inv_animation(animat, speed=SPEED.FAST):
    for i in range(len(animat)):
        left_eye.draw_animation_no_inv(iter_number=i, animation=animat, draw=False)
        right_eye.draw_animation_no_inv(iter_number=i, animation=animat, draw=False)
        right_eye.draw()
        sleep(speed.value)
    
def play_individual_eye_animation(animat, speed=SPEED.FAST):
    for i in range(len(animat)):
        left_eye.draw_individual_animation(iter_number=i, animation=animat, draw=False)
        right_eye.draw_individual_animation(iter_number=i, animation=animat, draw=False)
        right_eye.draw()
        sleep(speed.value)

"""
play_non_inv_animation(LOOK_AROUND)
play_animation(LOOK_AROUND_TO_FALLING)
play_animation(FALLING)
for i in range(4):
    play_individual_eye_animation(FIGURE_EIGHT, speed=SPEED.FASTER)
# play_animation(ANIMATION_FALLING_TO_LOOK_AROUND)
# play_non_inv_animation(ANIMATION_LOOK_AROUND)
# play_non_inv_animation(ANIMATION_LOOK_AROUND_TO_CORNER_FLASHER)
# play_animation(ANIMATION_CORNER_FLASHER)
# play_animation(ANIMATION_CORNER_FLASHER_TO_SPINNER)
# play_animation(ANIMATION_SPINNER)
# play_individual_eye_animation(ANIMATION_SPINNER_TO_FIGURE_EIGHT)
# for i in range(4):
    # play_individual_eye_animation(ANIMATION_FIGURE_EIGHT, speed=SPEED.FASTER)
"""