
PANEL_ORDER = list(range(73))
from raspberry_pi_controller.transmitter import LEDPacket, Transmitter
from raspberry_pi_controller.constants import MAPPING, WIDTH, HEIGHT
from raspberry_pi_controller.image_handling.image_handler import ImageHandler
from raspberry_pi_controller.effects.image_effect import ImageEffect
from raspberry_pi_controller.effects.two_color_random_effect import TwoColorRandom
from raspberry_pi_controller.effects.audio_effect import AudioEffect
from raspberry_pi_controller.ntfy_listener import NTFYListener
from raspberry_pi_controller.frame import Frames
from PIL import Image
import numpy as np
from time import sleep, perf_counter


class Panel:
    NUM_PIXELS = 73
    def __init__(self):
        self.transmitter = Transmitter()
        self.ntfy_listener = NTFYListener()
        self.ntfy_listener.start_thread()
        self.image_handler = ImageHandler()
        self.effects_list = [
            ImageEffect(),
            TwoColorRandom(),
            AudioEffect()
        ]
        self.accepted_commands = {
            "SET_ARDUINO_PGAIN": self.set_arduino_p_gain
        }
        self.arduino_ramp_rate = 10

    def set_image(self, image_name: str = "Sample.png", frame: int = None):
        pixels = [(0, 0, 0) for _ in range(73)]
        # Convert the resized image to a NumPy array
        image_array = self.image_handler.open_saved_image(image_name, frame=frame)
        # Iterate through the pixels and print RGB values
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if MAPPING[y][x] is not None:
                    pixel = image_array[y, x]
                    pixel_number = MAPPING[y][x]
                    pixels[pixel_number] = pixel[:3]
                # r, g, b = pixel[:3]  # Extract the RGB values
                # print(f"Pixel at ({x}, {y}): R={r}, G={g}, B={b}")
        self.write(pixels)

    def set_single_pixel(self, pixel_id: int, color_setpoint = tuple) -> list:
        pixels = list()
        for i in range(73):
            color = color_setpoint if i == pixel_id else (0, 0, 0)
            pixels.append(color)
        print(pixels)
        self.write(pixels)
        return pixels
    
    def set_color(self, color: tuple):
        pixels = [color for i in range(self.NUM_PIXELS)]
        self.write(color_list=pixels)

    def handle_commands(self):
        commands = self.ntfy_listener.get_queue()
        for command in commands:
            for effect in self.effects_list:
                for accepted_command in effect.accepted_commands:
                    if accepted_command in command:
                        effect.accepted_commands[accepted_command](command)
            for accepted_command in self.accepted_commands:
                if accepted_command in command:
                    self.accepted_commands[accepted_command](command)

    def set_arduino_p_gain(self, command: str):
        try:
            ramp_rate = int(command.split("-")[1])
            self.arduino_ramp_rate = ramp_rate
            print(f"Ramp Rate Set {ramp_rate}")
        except Exception as e:
            print(e)
            self.arduino_ramp_rate = 20


    def run(self):
        # self.effects_list[0].set_image("0-https://i.gifer.com/embedded/download/2QeW.gif")
        while True:
            start_time = perf_counter()
            self.handle_commands()
            frames = Frames(frames=[effect.get_frame() for effect in self.effects_list])
            string_data = frames.get_string_data()
            end_time = perf_counter()
            # print(f"Frame Time: {end_time - start_time:.4f}s")
            self.write(string_data)
            sleep(0.01)
                
    def write(self, color_list: list):
        base_list = [(0, 0, 0) for i in range(10)]
        for i in range(8):
            index = i*10
            for i in range(10):
                if index+i < len(color_list):
                    base_list[i] = color_list[index+i]

            packet = LEDPacket(index, self.arduino_ramp_rate, base_list)
            self.transmitter.send_packet(packet)
    
    def power_down(self):
        print("Attempting to power down")
        self.transmitter.power_down()
        print("Transmitter powered down")
        self.ntfy_listener.stop_thread()
