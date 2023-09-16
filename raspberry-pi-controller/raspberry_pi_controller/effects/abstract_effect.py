from raspberry_pi_controller.constants import WIDTH, HEIGHT
from raspberry_pi_controller.frame import Frame
from time import perf_counter
import numpy as np

class Effect:
    ACCEPTED_COMMANDS = list()

    def __init__(self):
        self.current_time = perf_counter()
        self.previous_call_time = perf_counter()
        self.gain = 0
        shape = (WIDTH, HEIGHT)
        value = (0, 0, 0)
        self.empty_frame = Frame(np.array([[value for _ in range(shape[0])] for _ in range(shape[1])]))

    def get_frame(self) -> Frame:
        raise NotImplementedError
    