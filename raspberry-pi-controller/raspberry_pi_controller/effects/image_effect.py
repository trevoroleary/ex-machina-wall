from raspberry_pi_controller.effects.abstract_effect import Effect
from raspberry_pi_controller.constants import WIDTH, HEIGHT
from raspberry_pi_controller.frame import Frame
from pathlib import Path
import urllib.request
import numpy as np
from PIL import Image, ImageEnhance
from time import perf_counter


class ImageEffect(Effect):
    _TEMP_STORAGE = r'/home/pi/repos/ex-machina-wall/raspberry-pi-controller/raspberry_pi_controller/image_handling/downloads'

    def __init__(self) -> None:
        super().__init__()
        self.accepted_commands = {
            "SET_IMAGE_URL": self.set_image,
            "SET_FRAME_TIME": self.set_frame_time,
            "SET_IMAGE_BRIGHTNESS": self.set_brightness
        }
        self.current_image: Image = None
        self.current_frame = None
        self.n_frames = None
        self.image_is_animated = False
        self.frame_time = 0.1
        self.brightness = 1
        pass
    
    def set_frame_time(self, command: str):
        try:
            frame_time = float(command.split('-')[1])
            self.frame_time = frame_time
            print(f"Frame time set {self.frame_time}")
        except Exception as e:
            print(e)
            pass

    def set_brightness(self, command: str):
        try:
            brightness = int(command.split("-")[1])
            self.brightness = brightness/100
            print(f"Set Image Brightness {brightness}")
        except Exception as e:
            print(e)
            pass

    def set_image(self, command: str):
        url = command.split("-")[1]
        if not url:
            self.current_image = None
            self.n_frames = None
            self.image_is_animated = False
            self.current_frame = None
        else:
            downloaded_image = self._get_image_from_url(url=url)
            # If downloading the image from a url fails set the current image to None
            if not downloaded_image:
                return self.set_image("-")
            
            self.current_image = downloaded_image
            if self.current_image.is_animated:
                self.n_frames = self.current_image.n_frames
                self.image_is_animated = True
                self.current_frame = 1
            else:
                self.n_frames = None
                self.image_is_animated = False
                self.current_frame = None
            print("New Image Set!")

    def get_frame(self) -> Frame:
        if self.current_image is None:
            return self.empty_frame
        elif self.image_is_animated:
            # Update the frame times
            self.current_time = perf_counter()
            if self.current_time - self.previous_call_time > self.frame_time:
                self.current_frame = ((self.current_frame + 1) % self.n_frames)
                # print(f"Updating current frame to {self.current_frame} | n_frames: {self.n_frames}")
                self.previous_call_time = self.current_time
                
                # For some reason 0 does not work
                self.current_frame = self.current_frame if self.current_frame else 1

            self.current_image.seek(self.current_frame)
            image = self.current_image.convert('RGB')
            converter = ImageEnhance.Color(image)
            frame = converter.enhance(4)
            frame = frame.resize((WIDTH, HEIGHT))
            # frame.save(Path(self._TEMP_STORAGE, "converted.png"))
        else:
            frame = self.current_image.resize((WIDTH, HEIGHT))
        image_array = (np.array(frame) * self.brightness).astype(int)
        frame = Frame(pixel_array=image_array)
        return frame

    def _get_image_from_url(self, url: str) -> Image:
        download_path = Path(self._TEMP_STORAGE, "downloaded_image.png")
        try:
            urllib.request.urlretrieve(url, download_path)
        except:
            return None
        image = Image.open(download_path)
        return image