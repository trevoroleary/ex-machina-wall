
from raspberry_pi_controller.websocket_transmitter import WebsocketTransmitter
from raspberry_pi_controller.image_handling.image_handler import ImageHandler
from raspberry_pi_controller.effects import AudioEffect, TwoColorRandom, ImageEffect, AudioEffect2
from raspberry_pi_controller.ntfy_listener import NTFYListener
from raspberry_pi_controller.frame import Frames, Frame
from raspberry_pi_controller.constants import NUM_PIXELS

from time import sleep, perf_counter
import logging
import struct

class Panel:
    NUM_PIXELS = 73
    TARGET_FRAME_TIME = 1/60
    def __init__(self):
        self.logger = logging.getLogger("Panel")
        self.web_socket_transmitter = WebsocketTransmitter()
        self.ntfy_listener = NTFYListener()
        self.ntfy_listener.start_thread()
        self.image_handler = ImageHandler()
        self.effects_list = [
            ImageEffect(),
            TwoColorRandom(),
            # AudioEffect2()
            # AudioEffect()
        ]
        self.modifiers_list = [
            AudioEffect2()
        ]
        # self.audio_effect = AudioEffect()
        self.accepted_commands = {
            "SET_ARDUINO_PGAIN": self.set_arduino_p_gain
        }
        self.arduino_ramp_rate = 10

    def handle_commands(self):
        """
        Get the commands out of the NTFY listener and pass them on to the effects that need them
        """
        # Get commands out of ntfy listener
        commands = self.ntfy_listener.get_queue()

        # iterate through the commands
        for command in commands:

            # Iterate through each effect we have and check if they listen to that command
            for effect in self.effects_list + self.modifiers_list:
                for accepted_command in effect.accepted_commands:
                    if accepted_command in command:
                        # If an effect listens to one of those commands pass it on in the relevant function
                        effect.accepted_commands[accepted_command](command)
            
            # Check if any of the commands are for this panel directly, rather than the effects
            for accepted_command in self.accepted_commands:
                if accepted_command in command:
                    self.accepted_commands[accepted_command](command)
            
            # for accepted_command in self.audio_effect.accepted_commands:
            #     if accepted_command in command:
            #         self.audio_effect.accepted_commands[accepted_command](command)

    def set_arduino_p_gain(self, command: str):
        """
        This is a command handler
        In each message there is a gain param for how quickly the arduino should reach the target color
        Parse the command and se
        """
        try:
            ramp_rate = int(command.split("-")[1])
            self.arduino_ramp_rate = ramp_rate
            self.logger.info(f"Ramp rate Updated to: {ramp_rate}")
        except Exception as e:
            self.logger.error(f"Failed to parse Arduino P Gain Command. ErrorL '{e}'")
            self.logger.error(f"'{command}' was not a valid command")
            self.logger.debug(f"Setting Arduino P Gain to default value of 20")
            self.arduino_ramp_rate = 20

    def run(self):
        while True:
            start_time = perf_counter()
            self.handle_commands()
            frame = Frames(frames=[effect.get_frame() for effect in self.effects_list])
            for modifier in self.modifiers_list:
                frame = modifier.get_frame(current_frame=frame.pixel_array)
            string_data = frame.get_string_data()
            end_time = perf_counter()
            self.web_socket_transmitter.send(self.get_payload(string_data))
            duration = end_time - start_time
            # self.logger.debug(f"Frame Time: {duration:.4f}s")
            if duration < self.TARGET_FRAME_TIME:
                sleep(self.TARGET_FRAME_TIME - duration)
    
    def get_payload(self, color_list) -> bytes:
        string_format = "@" + "".join(["B" for _ in range((NUM_PIXELS*3) + 1)])

        led_rgb_list = list()
        for r, g, b in color_list:
            led_rgb_list += [r, g, b]
        args = [self.arduino_ramp_rate] + led_rgb_list
        payload = struct.pack(string_format, *args)
        return payload

    def power_down(self):
        self.logger.info("Attempting to power down")
        self.ntfy_listener.stop_thread()
