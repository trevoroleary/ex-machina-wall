# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import threading
from segment import Segment
from enum import Enum
from enums import COLORS, SPEED, ColorGenerator

class SegmentManager:

    def __init__(self):
        self.segments = list()
        self.pixels_strip = None
        # self.pixels_strip = neopixel.NeoPixel(
            # board.D18, 
            # 30*5,
            # brightness=0.1,
            # auto_write=False,
            # pixel_order=neopixel.RGBW
        # )

        # seg_1 = Segment(pixels=self.pixels_strip, start_position=0, end_position=30)
        # seg_2 = Segment(pixels=self.pixels_strip, start_position=30, end_position=60)
        # seg_3 = Segment(pixels=self.pixels_strip, start_position=60, end_position=90)
        # seg_4 = Segment(pixels=self.pixels_strip, start_position=90, end_position=120)
        # seg_5 = Segment(pixels=self.pixels_strip, start_position=120, end_position=150)
        # self.segments = [seg_1, seg_2, seg_3, seg_4, seg_5]
              
        self.pixels_ring = neopixel.NeoPixel(
            board.D21, 
            48,
            brightness=0.1,
            auto_write=False,
            pixel_order=neopixel.RGB
        )
        glasses_1 = Segment(pixels=self.pixels_ring, start_position=0, end_position=24, glasses_left=True)
        glasses_2 = Segment(pixels=self.pixels_ring, start_position=24, end_position=48, glasses_right=True)
        self.segments.extend([glasses_1, glasses_2])


    def call_on_all(self, func_name: str, kwargs: dict, draw=True):
        for segment in self.segments:
            getattr(segment, func_name)(**kwargs)
        if draw:
            if self.pixels_strip:
                self.pixels_strip.show()
            self.pixels_ring.show()
    
    def pulse(self):
        for i in range(100):
            for segment in self.segments:
                segment.sync_sweep_right(percentage=i, color_on=COLORS.RED, color_off=COLORS.OFF)
            self.draw()
    
    def turn_off(self):
        for segment in self.segments:
            segment.set_all(color=COLORS.OFF)
        self.draw()

    def call_on_segment(self, func_name: str, segment_index: int, kwargs: dict, draw: bool = True):
        getattr(self.segments[segment_index], func_name)(**kwargs)
        if draw:
            self.pixels_strip.show()
            self.pixels_ring.show()
    
    def draw(self, sleep_time: float = 0):
        if self.pixels_strip:
            self.pixels_strip.show()
        self.pixels_ring.show()
        if sleep_time:
            time.sleep(sleep_time)

    def wheel_around(self, speed: float):
        # Wheel around all of them
        for i in range(2*len(self.segments)):
            for segment_index in range(len(self.segments)):
                if segment_index == (i % len(self.segments)):
                    color = COLORS.RED_BLUE
                else:
                    color = COLORS.OFF
                self.call_on_segment('set_all', segment_index=segment_index, draw=False, kwargs={'color': color})
            self.draw(speed)

    def sweep_colors(self, multiplier: float = 1):
        for i in range(10000):
            self.call_on_all('set_time_color', kwargs={'multiplier': multiplier})
            time.sleep(SPEED.FASTEST.value)

    def flash(self, iter_number: int, mod_number: int, color_on, color_off):
        color = color_off
        if iter_number % mod_number > mod_number/2:
            color = color_on
        for segment in self.segments:
            segment.set_all(color=color)
        self.draw()