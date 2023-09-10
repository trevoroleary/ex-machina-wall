from raspberry_pi_controller.effects.abstract_effect import Effect
from raspberry_pi_controller.constants import WIDTH, HEIGHT
from raspberry_pi_controller.frame import Frame
import numpy as np


class TwoColorRandom(Effect):
    FRAME_TIME = 0.1

    def __init__(self) -> None:
        super().__init__()
        self.accepted_commands = {
            "SET_PRIMARY": self.set_primary,
            "SET_SECONDARY": self.set_secondary,
            "SET_BRIGHTNESS": self.set_brightness
        }
        self.primary_color = (0, 0, 0)
        self.secondary_color = (0, 0, 0)
        self.brightness = 1

    @property
    def primary_color_scaled(self) -> tuple:
        scaled = (
            int(self.primary_color[0]*self.brightness), 
            int(self.primary_color[1]*self.brightness),
            int(self.primary_color[2]*self.brightness)
            )
        return scaled

    def set_brightness(self, command: str):
        split_command = command.split("-")
        self.brightness = int(split_command[1])/100

    def set_primary(self, command: str):
        split_command = command.split('-')
        r = int(split_command[1])
        g = int(split_command[2])
        b = int(split_command[3])
        self.primary_color = (r, g, b)
    
    def set_secondary(self, command: str):
        self.secondary_color = (0, 255, 0)

    def get_frame(self) -> Frame:
        frame = Frame(np.array([[self.primary_color_scaled for _ in range(WIDTH)] for _ in range(HEIGHT)]))
        return frame
