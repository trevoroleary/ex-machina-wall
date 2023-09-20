from raspberry_pi_controller.effects.abstract_effect import Effect
from raspberry_pi_controller.constants import WIDTH, HEIGHT
from raspberry_pi_controller.frame import Frame
from pathlib import Path
import urllib.request
import numpy as np
from PIL import Image, ImageEnhance
from time import perf_counter
from raspberry_pi_controller.image_handling.favorite_images import FAVORITES
import logging 


class ImageEffect(Effect):
    _TEMP_STORAGE = r'/home/pi/repos/ex-machina-wall/raspberry-pi-controller/raspberry_pi_controller/image_handling/downloads'
    MAX_TIME_ON_IMAGE = 2*60
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger("ImageEffect")
        self.accepted_commands = {
            "SET_IMAGE_URL": self.set_image,
            "SET_FRAME_TIME": self.set_frame_time,
            "SET_IMAGE_BRIGHTNESS": self.set_brightness
        }

        # Variables related to cycling images
        self._saved_favourite_images = {}
        self.last_image_change_time = perf_counter()
        self.image_index = 0

        self.current_image: Image = None
        self.current_frame = None
        self.n_frames = None
        self.image_is_animated = False
        self.frame_time = 0.1
        self.brightness = 100
        pass
    
    def set_frame_time(self, command: str):
        try:
            frame_time = float(command.split('-')[1])
            self.frame_time = frame_time
            print(f"Frame time set {self.frame_time}")
        except Exception as e:
            print(e)
            self.frame_time = 0.1

    def set_brightness(self, command: str):
        try:
            brightness = int(command.split("-")[1])
            self.brightness = brightness
            print(f"Set Image Brightness {brightness}")
        except Exception as e:
            print(e)
            self.brightness = 100
            pass

    def set_image(self, command: str):
        url = command.split("-")[1]
        if not url:
            self.current_image = None
            self.n_frames = None
            self.image_is_animated = False
            self.current_frame = None
        else:
            self._handle_image_url(url=url)

    def _handle_image_url(self, url: str):
        self.last_image_change_time = perf_counter()
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
        self.logger.info("New Image Set!")
        
    def set_next_image(self):
        self.image_index = (self.image_index + 1) % len(FAVORITES)
        image_url = FAVORITES[self.image_index]
        if image_url in self._saved_favourite_images:
            self.last_image_change_time = perf_counter()
            self.current_image = self._saved_favourite_images[image_url]
            if self.current_image.is_animated:
                self.n_frames = self.current_image.n_frames
                self.image_is_animated = True
                self.current_frame = 1
            else:
                self.n_frames = None
                self.image_is_animated = False
                self.current_frame = None
        else:
            self._handle_image_url(image_url)
            self._saved_favourite_images[image_url] = self.current_image

    def get_frame(self) -> Frame:
        """
        This is the main call that returns a frame of the GIF
        """
        # If the current image is None, or in otherwords this effect is disabled, we return an empty frame
        if self.current_image is None:
            return self.empty_frame

        # If we have been showing this image for too long cycle the image
        if perf_counter() - self.last_image_change_time > self.MAX_TIME_ON_IMAGE:
            self.logger.debug(f"Cyling GIF Automatically")
            self.set_next_image()

        # If the image is animated we will be keeping in mind frame times and updating accordingly
        if self.image_is_animated:
            # Update the frame times
            current_time = perf_counter()
            if current_time - self.previous_call_time > self.frame_time:
                self.current_frame = ((self.current_frame + 1) % self.n_frames)
                # print(f"Updating current frame to {self.current_frame} | n_frames: {self.n_frames}")
                self.previous_call_time = current_time
                
                # For some reason 0 does not work so just make sure we don't pick 0th frame
                self.current_frame = self.current_frame if self.current_frame else 1
            
            # Get the frame, resize it, and enhance it
            self.current_image.seek(self.current_frame)
            image = self.current_image.convert('RGB')
            converter = ImageEnhance.Color(image)
            frame = converter.enhance(4)
            frame = frame.resize((WIDTH, HEIGHT))
            # frame.save(Path(self._TEMP_STORAGE, "converted.png"))
        else:
            frame = self.current_image.resize((WIDTH, HEIGHT))
        image_array = np.array(frame) * (self.brightness/100)
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