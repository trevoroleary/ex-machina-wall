import time

from segment_manager import SegmentManager
from enums import SPEED, COLORS, ColorGenerator, MODES

import sys
import time
import RPi.GPIO as GPIO
from threading import Thread

class HalloweenCostume:
    def __init__(self):
        self.led_manager = SegmentManager()
        self.color_on = COLORS.RED
        self.color_off = COLORS.OFF
        self.speed = SPEED.FAST
        self.current_pattern = MODES.SKIP_SOME
        self.previous_pattern = MODES.SKIP_SOME

        self.mode_switch_pin_number = 2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.mode_switch_pin_number, GPIO.IN)

        GPIO.add_event_detect(self.mode_switch_pin_number, GPIO.FALLING, callback=self.next_mode)
        threads = list()
        threads.append(Thread(target=self.change_color))

        for thread in threads:
            thread.start()

        self.run()

    def change_color(self):
        while True:
            self.color_on = COLORS.random_color()
            time.sleep(1)

    def run(self):
        i = 0
        while True:
            if self.current_pattern == MODES.SKIP_SOME:
                if self.new_pattern:
                    i = 0
                i = 0 if i >= 50 else i
                # Skip Some Moving Across Line
                self.led_manager.call_on_all(
                    func_name='skip_some', 
                    kwargs={'iter_number': i, 'skip_length': 8, 'color_on': self.color_on, 'color_off': self.color_off})
                time.sleep(self.speed.value)
            elif self.current_pattern == MODES.PULSE:
                # Thread is listening for button presses already
                continue
            elif self.current_pattern == MODES.FLASH:
                if self.new_pattern:
                    i = 0
                self.led_manager.flash(iter_number=i, mod_number=5, color_on=self.color_on, color_off=self.color_off)
                time.sleep(self.speed.value)
            elif self.current_pattern == MODES.BUILD:
                if self.new_pattern:
                    i = 0
                i = 0 if i >=100 else i
                self.led_manager.call_on_all(func_name='sync_sweep_right', kwargs={'percentage': i, 'color_on': COLORS.RED_BLUE, 'color_off': COLORS.OFF})
                time.sleep(SPEED.FASTEST.value)
            elif self.current_pattern == MODES.NOTHING:
                i = 0
                self.led_manager.turn_off()
                time.sleep(SPEED.SLOW.value)
            i += 1

    def next_mode(self, _):
        self.current_pattern = self.current_pattern.succ()

    @property
    def new_pattern(self) -> bool:
        if self.current_pattern != self.previous_pattern:
            self.previous_pattern = self.current_pattern
            return True
        return False

HalloweenCostume()