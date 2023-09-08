import pygame
from pygame.event import Event
from typing import List
from wall_emulator.global_game_variable import Global


class Slider:
    def __init__(self, canvas, position_x, position_y):
        self.v = Global()
        self.rectangle = pygame.rect.Rect(position_x, position_y, 17, 17)
        self.rectangle_dragging = False
        self.canvas = canvas
        self.offset_x = 0
        self.offset_y = 0
        self.old_screen_x = None
        self.old_screen_y = None
        self.x_min = position_x
        self.x_max = position_x + 100

    @property
    def amount(self) -> float:
        percentage = self.rectangle.x - self.x_min
        return percentage

    def handle_events(self, events: List[Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rectangle.collidepoint(event.pos):
                        self.rectangle_dragging = True
                        mouse_x, mouse_y = event.pos
                        self.offset_x = self.rectangle.x - mouse_x
                        # self.offset_y = self.rectangle.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.rectangle_dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if self.rectangle_dragging:
                    mouse_x, mouse_y = event.pos
                    new_x = mouse_x + self.offset_x
                    if self.x_min < new_x < self.x_max:
                        self.rectangle.x = mouse_x + self.offset_x
                    # self.rectangle.y = mouse_y + self.offset_y

    def draw(self, screen_width: int, screen_height: int):
        if self.old_screen_x is None:
            self.old_screen_x = screen_width
        else:
            difference = screen_width - self.old_screen_x
            self.rectangle.x = self.rectangle.x + difference
            self.old_screen_x = screen_width
        if self.old_screen_y is None:
            self.old_screen_y = screen_height
        else:
            difference = screen_height - self.old_screen_y
            self.rectangle.y = self.rectangle.y + difference
            self.old_screen_y = screen_height
        pygame.draw.rect(surface=self.canvas, color=pygame.Color("blue"), rect=self.rectangle)
