import numpy as np
from raspberry_pi_controller.constants import HEIGHT, WIDTH, MAPPING, NUM_PIXELS
from typing import List


class Frame:
    def __init__(self, pixel_array: np.array):
        self.pixel_array = pixel_array

    def _get_string_data(self) -> list: 
        pixels = [(0, 0, 0) for _ in range(NUM_PIXELS)]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if MAPPING[y][x] is not None:
                    pixel = self.pixel_array[y, x]
                    pixel_number = MAPPING[y][x]
                    pixels[pixel_number] = pixel[:3]
        return pixels

class Frames:
    def __init__(self, frames: List[Frame]):
        self.frames = frames
    
    def get_string_data(self) -> list:
        sum_frame = None
        for frame in self.frames:
            if sum_frame is None:
                sum_frame = frame.pixel_array
            else:
                sum_frame = sum_frame + frame.pixel_array
        sum_frame = np.clip(sum_frame, 0, 255)
        return self._get_string_data(numpy_pixels=sum_frame)

    def _get_string_data(self, numpy_pixels: np.array) -> list: 
        pixels = [(0, 0, 0) for _ in range(NUM_PIXELS)]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if MAPPING[y][x] is not None:
                    pixel = numpy_pixels[y, x]
                    pixel_number = MAPPING[y][x]
                    pixels[pixel_number] = pixel[:3]
        return pixels