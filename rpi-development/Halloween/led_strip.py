# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import threading
from appendage import Appendage
from color_profiles import ColorProfiles

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 30*4

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGBW

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


APPENDAGES = {
    "RIGHT_LEG": range(1, 30),
    "LEFT_LEG": range(30, 60),
    "RIGHT_ARM": range(60, 90),
    "LEFT_ARM": range(90, 120)
}

profile_generator = ColorProfiles()

right_leg = Appendage(pixels=pixels, pixel_list=APPENDAGES['RIGHT_LEG'])
left_leg = Appendage(pixels=pixels, pixel_list=APPENDAGES['LEFT_LEG'])
right_arm = Appendage(pixels=pixels, pixel_list=APPENDAGES['RIGHT_ARM'])
left_arm = Appendage(pixels=pixels, pixel_list=APPENDAGES['LEFT_ARM'])
appendates = [right_leg, left_leg, left_arm, right_arm]

threads = list()
for appendage in appendates:
    pulse_profile = profile_generator.color_wheel_range(0, len(appendage.pixel_locations))
    threads.append(threading.Thread(target=appendage.pulse, args=([0.5, pulse_profile])))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()


def pulse():
    for i in range(num_pixels):
        pixels[i] = wheel(0)
        pixels.show()
        time.sleep(0.001)
    color = wheel(20)
    for i in range(num_pixels-1, -1, -1):
        pixels[i] = color
        pixels.show()
        time.sleep(0.001)
    

def wheel(pos):
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
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


for i in range(1):
    demo = False
    if demo:
        # Comment this line out if you have RGBW/GRBW NeoPixels
        # pixels.fill((255, 0, 0))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        pixels.fill((255, 0, 0, 0))
        pixels.show()
        time.sleep(1)

        # Comment this line out if you have RGBW/GRBW NeoPixels
        # pixels.fill((0, 255, 0))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        pixels.fill((0, 255, 0, 0))
        pixels.show()
        time.sleep(1)

        # Comment this line out if you have RGBW/GRBW NeoPixels
        # pixels.fill((0, 0, 255))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        pixels.fill((0, 0, 255, 0))
        pixels.show()
        time.sleep(1)

    pulse()

    # rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
pixels[0:num_pixels] = [(0, 0, 0, 0)] * num_pixels
pixels.show()
