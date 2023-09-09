from enums import COLORS
from threading import Thread
from time import sleep
from behaviour_lists import MAIN_ANIMATIONS
from behaviour_lists import *
from eye import Eye
import neopixel
import board
from enums import SPEED
import random 
import RPi.GPIO as GPIO
import time
import multiprocessing


GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class Manager:
    def __init__(self):

        GPIO.add_event_detect(2, GPIO.FALLING, callback=self.pulse, bouncetime = 500)

        self.last_time_pulse_was_hit = -4
        self.next_color = COLORS.RED.value['RGB']
        color_update_thread = Thread(target=self.update_colors)
        set_new_color_target = Thread(target=self.set_new_color_target)
        run_animations_thread = Thread(target=self.run_animations)
        check_pulse_over_thread = Thread(target=self.check_pulse)

        threads = [color_update_thread, set_new_color_target, run_animations_thread]
        pixels_ring = neopixel.NeoPixel(
            board.D21, 
            48,
            brightness=0.07,
            auto_write=False,
            pixel_order=neopixel.RGB
        )
        self.left_eye = Eye(pixels=pixels_ring, start_position=0, end_position=24, left=True)
        self.right_eye = Eye(pixels=pixels_ring, start_position=24, end_position=48, right=True)
        self.left_eye.set_all(color=(0,0,0), draw=True)
        self.right_eye.set_all(color=(0,0,0), draw=True)

        self.pulsing = False
        self.pulsing_now = False
        self.pulse_thread = None

        color_update_thread.start()
        set_new_color_target.start()
        run_animations_thread.start()
        check_pulse_over_thread.start()

    def run_animations(self):
        old_animation_name = random.choice(list(MAIN_ANIMATIONS))
        new_animation_name = random.choice(list(MAIN_ANIMATIONS))
        transition_name = None
        while True:
            if old_animation_name == new_animation_name:
                transition_name = None
            else:
                transition_name = old_animation_name + "_TO_" + new_animation_name
            
            if transition_name:
                animation = globals()[transition_name]
                if len(animation[0]) == 2:
                    self.play_individual_eye_animation(animation)
                elif "INV" in transition_name:
                    self.play_non_inv_animation(animation)
                else:
                    self.play_animation(animation)
            
            animation = globals()[new_animation_name]
            if "INV" in new_animation_name:
                self.play_non_inv_animation(animation)
            elif len(animation[0]) == 2:
                self.play_individual_eye_animation(animation)
            else:
                self.play_animation(animation)
            old_animation_name = random.choice(list(MAIN_ANIMATIONS))
            new_animation_name = random.choice(list(MAIN_ANIMATIONS))

    def play_animation(self, animat, speed=SPEED.FAST, allow=False):
        for i in range(len(animat)):
            if self.pulsing and not allow:
                return True
            self.left_eye.draw_animation(iter_number=i, animation=animat, draw=False)
            self.right_eye.draw_animation(iter_number=i, animation=animat, draw=False)
            self.right_eye.draw()
            sleep(speed.value)

    def play_non_inv_animation(self, animat, speed=SPEED.FAST):
        for i in range(len(animat)):
            if self.pulsing:
                return True
            self.left_eye.draw_animation_no_inv(iter_number=i, animation=animat, draw=False)
            self.right_eye.draw_animation_no_inv(iter_number=i, animation=animat, draw=False)
            self.right_eye.draw()
            sleep(speed.value)
        
    def play_individual_eye_animation(self, animat, speed=SPEED.FAST):
        for i in range(len(animat)):
            if self.pulsing:
                return True
            self.left_eye.draw_individual_animation(iter_number=i, animation=animat, draw=False)
            self.right_eye.draw_individual_animation(iter_number=i, animation=animat, draw=False)
            self.right_eye.draw()
            sleep(speed.value)

    def set_new_color_target(self):
        while True:
            self.next_color = COLORS.random_color().value['RGB']
            sleep(10)

    def update_eye_colors(self, color):
        r, g, b = color
        self.right_eye.colors = [(0,0,0), (int(r/5), int(g/5), int(b/5)), color]
        self.left_eye.colors = self.right_eye.colors

    def update_colors(self):
        while True:
            r_next, g_next, b_next = self.next_color
            new_r, new_g, new_b = self.right_eye.colors[2]
            r, g, b = self.right_eye.colors[2]
            r_add = 1 if r < r_next else -1 if r > r_next and sum([r,g,b]) > 50 else 0
            new_r += r_add
            g_add = 1 if g < g_next else -1 if g > g_next and sum([r,g,b]) > 50 else 0
            new_g += g_add
            b_add = 1 if b < b_next else -1 if b > b_next and sum([r,g,b]) > 50 else 0
            new_b += b_add
            self.update_eye_colors((new_r, new_g, new_b))           
            sleep(0.05)

    def pulse(self, x):
        GPIO.remove_event_detect(2)
        self.last_time_pulse_was_hit = time.perf_counter()
        self.pulsing = True
        self.right_eye.stop = True
        self.left_eye.stop = True

        
        pulse_animation_name = random.choice(PULSE_NAMES)
        pulse_animation = globals()[pulse_animation_name]
        if 'SLOWER' in pulse_animation_name:
            speed = SPEED.SLOW
        else:
            speed = SPEED.FASTEST
        self.play_animation(pulse_animation, speed=speed, allow=True)
        # self.left_eye.set_all(color=(0,0,0), draw=True)
        # self.right_eye.set_all(color=(0,0,0), draw=True)
        GPIO.add_event_detect(2, GPIO.FALLING, callback=man.pulse, bouncetime = 500)

    
    def check_pulse(self):
        while True:
            if time.perf_counter() - self.last_time_pulse_was_hit > 5:
                self.pulsing = False
            sleep(1)

man = Manager()

