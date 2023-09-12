from raspberry_pi_controller.constants import WIDTH, HEIGHT
from raspberry_pi_controller.frame import Frame
from random import randrange
from time import perf_counter
import numpy as np
from math import sqrt


class AudioEffect:

    def __init__(self):
        self.accepted_commands = {}
        self.current_time = perf_counter()
        self.previous_call_time = perf_counter()
        self.gain = 0
        self.np_frame = np.array([[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)])
        self.most_recent_audio_level = 0
        self.current_color = (0, 0, 255)
        self.target_range = 500
        self.target_ranges = list()

    # def get_frame(self) -> Frame:
    #     self.most_recent_audio_level = randrange(0, 110, 1)
    #     if self.most_recent_audio_level > 100:
    #         self.np_frame = np.array([[self.current_color for _ in range(WIDTH)] for _ in range(HEIGHT)])
    #     else:
    #         self.np_frame = self.np_frame / 1.2
    #     return Frame((self.np_frame).astype(int))

    def get_frame(self) -> Frame:
        self.most_recent_audio_level = randrange(0, 110, 1)
        if self.most_recent_audio_level > 100:
            self.target_ranges.append(0)
            self.target_range = 0
        else:
            pop_list = list()
            for i in range(len(self.target_ranges)):
                self.target_ranges[i] += 20
                if self.target_ranges[i] > 500:
                    pop_list.append(i)
            pop_list.sort(reverse=True)
            for i in pop_list:
                self.target_ranges.pop(i)
            self.target_range += 20
        y_offset = 6
        x_offset = 8
        self.np_frame = self.np_frame/1.2
        for y in range(HEIGHT):
            _y = y - y_offset
            for x in range(WIDTH):
                _x = x - x_offset
                distance = sqrt(_x**2 + _y**2)*10
                all_distance_errors = [abs(target - distance) for target in self.target_ranges]
                if all_distance_errors:
                    distance_error = min(all_distance_errors)
                    # distance_error = abs(self.target_range - distance)
                    self.np_frame[y][x] = (155 - (distance_error*5), 0, 0)
        return Frame(self.np_frame)


    def set_effect_gain(self, gain: float):
        self.gain = gain
