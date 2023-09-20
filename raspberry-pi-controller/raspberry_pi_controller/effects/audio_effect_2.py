from raspberry_pi_controller.constants import WIDTH, HEIGHT, complement
from raspberry_pi_controller.frame import Frame, Frames
from raspberry_pi_controller.audio_reactor.stream_analyzer import Stream_Analyzer
from time import perf_counter
import numpy as np
import logging
from math import sqrt

class AudioEffect2:
    PEAK_AMPLITUDE = 200000
    PEAK_BASS_AMPLITUDE = 300000

    def __init__(self):
        self.logger = logging.getLogger("AudioEffect2")
        self.accepted_commands = {
            "ENABLE_HF_REACT": self.set_hf_react_state,
            "ENABLE_LF_REACT": self.set_lf_react_state,
        }
        self.np_frame = np.array([[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)])
        self.stream_analyzer = Stream_Analyzer()
        self.high_color = (0, 0, 255)
        self.low_color = (255, 0, 0)
        self.hf_react_state = False
        self.lf_react_state = False

    def set_hf_react_state(self, command: str):
        try:
            state = command.split("-")[1]
            if state == "1":
                self.logger.info(f"Enabling HF Reacting: {state}")
            else:
                self.logger.info(f"Disabling HF React: {state}")
            self.hf_react_state = state == "1"
        except Exception as e:
            self.logger.error(e)
            self.logger.info("Disabling HF React")
            self.hf_react_state = False

    
    def set_lf_react_state(self, command: str):
        try:
            state = command.split("-")[1]
            if state == "1":
                self.logger.info(f"Enabling LF Reacting: {state}")
            else:
                self.logger.info(f"Disabling LF React: {state}")
            self.lf_react_state = state == "1"
        except Exception as e:
            self.logger.error(e)
            self.logger.info("Disabling LF React")
            self.lf_react_state = False

    def get_frame(self, current_frame: np.array = None) -> Frame:
        current_frame = current_frame if current_frame is not None else np.array([[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)])

        _, _, _, amplitudes = self.stream_analyzer.get_audio_features()

        current_frame = self.get_perimeter_pulse(current_frame, amplitudes)

        current_frame = self.add_bass_pulse(current_frame, amplitudes)

        return Frame(current_frame)
    
    def get_perimeter_pulse(self, current_frame, amplitudes) -> np.array:
        if not self.hf_react_state:
            return current_frame
        max_height = 7
        middle_point_x = 8
        for y in range(HEIGHT):
            for x in range(WIDTH):
                frame_color = self.high_color

                # We are in the top half need top down section
                if y <= max_height:  
                    if x <= middle_point_x:
                        amplitude = amplitudes[-x]
                    else:
                        amplitude = amplitudes[int(-middle_point_x + (-middle_point_x + x))]  
                    height = round(min(amplitude/self.PEAK_AMPLITUDE, 1) * max_height + 0.3)
                    if y < height:
                        current_frame[y][x] = frame_color
                # We are on the bottom half section
                else:  
                    if x <= middle_point_x:
                        amplitude = amplitudes[-x]
                    else:
                        amplitude = amplitudes[int(-middle_point_x + (-middle_point_x + x))]
                    height = round(min(amplitude/self.PEAK_AMPLITUDE, 1) * max_height + 0.3)
                    if (HEIGHT - y - 1) < height:
                        current_frame[y][x] = frame_color

        # self.logger.debug(f"Duration {end_time-start_time:.4f}s")
        return current_frame

    def add_bass_pulse(self, current_frame, amplitudes):
        if not self.lf_react_state:
            return current_frame
        max_height = 4

        amplitude = sum(amplitudes[:3])/len(amplitudes[:3])
        target_radius = round(min(amplitude/self.PEAK_BASS_AMPLITUDE, 1) * max_height)
        
        # Start drawing the circles
        y_offset = 6
        x_offset = 8
        for y in range(HEIGHT):
            _y = y - y_offset
            for x in range(WIDTH):
                _x = x - x_offset
                frame_color = self.low_color
                # frame_color = current_frame[y][x]
                # _x and _y are the corrected x, y so that we iterate around the center of the wall
                # Calculate the distance the current pixel we're setting is from the center of the screen
                distance = sqrt(abs(_x*2) + _y**2)
                if distance < target_radius:
                    # Draw the color in that location
                    current_frame[y][x] = frame_color

        # self.logger.debug(f"Duration {end_time-start_time:.4f}s")
        return current_frame

    # def get_frame(self) -> Frame:
    #     """
    #     This is the standard get frame, it just adds a fixed color, which can be set by secondary color
    #     """
    #     # Get the start time of the function for debugging purposes
    #     _, _, bins, amplitude = self.stream_analyzer.get_audio_features()
    #     self.np_frame = np.array([[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)])

    #     for y in range(HEIGHT):
    #         for x in range(WIDTH):
    #             y_max = int(min(amplitude[x]/200000, 1)*HEIGHT + 0.5)
    #             if y <= y_max:
    #                 self.np_frame[HEIGHT - y - 1][x] = (255, 0 ,0)
    #     # self.logger.debug(f"Duration {end_time-start_time:.4f}s")
    #     return Frame(self.np_frame)
