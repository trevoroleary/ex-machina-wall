import random
# Simple test for NeoPixels on Raspberry Pi
import numpy
import time
from typing import NoReturn
import board
import neopixel
ORDER = neopixel.RGBW


class Appendage:

    def __init__(self, pixels, pixel_list: list):
        self.pixels = pixels
        self.pixel_locations = pixel_list
        self.num_pixels = len(pixel_list)
        self.sync_start_time = None

        shift = int(self.num_pixels*0.5)
        self.saw_window = [max(((x - shift) / (self.num_pixels - 1), 0)) for x in range(self.num_pixels)]
    
    def sync_start(self):
        self.sync_start_time = time.perf_counter()
    
    def sync_check(self, sync_time: float):
        if self.sync_start_time is None:
            return
        stop_time = time.perf_counter()
        diff = sync_time - (stop_time - self.sync_start_time)
        if diff > 0:
            time.sleep(diff)

    def pulse(self, sync_time: float, color_list: list, back=True) -> bool:
        
        for shift in range(-self.num_pixels, self.num_pixels, -1):
            self.sync_start()
            
            # Generate Mask
            mask = self.get_saw_mask(shift=shift)
            mask.reverse()
            
            pixels_to_set = [self.scale_tuple(color_list[j], mask[j]) for j in range(self.num_pixels)]
            self.pixels[self.pixel_locations[0]: self.pixel_locations[-1]] = pixels_to_set
            self.pixels.show()
            self.sync_check(sync_time=sync_time)
        if back:
            for shift in range(-self.num_pixels, self.num_pixels):
                self.sync_start()
                mask = self.get_saw_mask(shift=shift, reverse=True)
                pixels_to_set = [self.scale_tuple(color_list[j], mask[j]) for j in range(self.num_pixels)]
                self.pixels[self.pixel_locations[0]: self.pixel_locations[-1]] = pixels_to_set
                self.pixels.show()
                self.sync_check(sync_time=sync_time)

        # for scaling in range(100, 0, -10):

            # for pixel in self.pixel_locations:
                # self.sync_start()

                # for prev_pix in range(pixel-1, self.pixel_locations[0], -1):
                    # self.pixels[prev_pix] = tuple([int(x*drop_off) for x in self.pixels[prev_pix]])
                # self.pixels[pixel] = color_list[pixel - self.pixel_locations[0]]
                # self.pixels.show()
                # self.sync_check(sync_time=sync_time)
    
    def scale_tuple(self, items_to_scale, scaler) -> tuple:
        return tuple([int(x*scaler) for x in items_to_scale])

    def get_saw_mask(self, shift: int, reverse: bool = False) -> list:
        if shift < 0:
            mask = self.shift_left(self.saw_window, n=shift)
        elif shift > 0:
            mask = self.shift_right(self.saw_window, n=shift)
        else:
            mask = self.saw_window
        return mask[:self.num_pixels]

    def shift_left(self, arr, n):
        return arr[-n:] + [0] * -n
    
    def shift_right(self, arr, n):
        return [0]*n + arr[:-n]

    def color_wheel(self, pos, scaler: float = 1.0):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (int(r*scaler), int(g*scaler), int(b*scaler), 0)
