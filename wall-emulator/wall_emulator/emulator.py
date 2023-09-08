from wall_emulator.slider import Slider
from wall_emulator.panel import Panels
from wall_emulator.utils import SCREEN_HEIGH, SCREEN_WIDTH, FPS, deg_to_rad
from wall_emulator.global_game_variable import Global
import pygame
from pygame import BLEND_RGB_ADD
from math import tan


class WallEmulator:
    def __init__(self):
        # self.position_slider = Slider(position_x=0, position_y=0, dimensions=2)

        pygame.init()
        # vec = pygame.math.Vector2  # 2 for two dimensional
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGH), pygame.RESIZABLE)
        pygame.display.set_caption(title="EX-MACHINA-EMULATOR")
        self.v = Global()
        self.spacing_slider = Slider(
            canvas=self.canvas,
            position_x=100,
            position_y=SCREEN_HEIGH-30
        )
        self.panels = Panels(canvas=self.canvas, starting_x=250, starting_y=150)

        self._object = [self.spacing_slider, self.panels]

    temp_surface = pygame.Surface((512, 512), pygame.SRCALPHA)

    def run(self):

        clock = pygame.time.Clock()
        running = True

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            self.v.x_spacing_adjust = self.spacing_slider.amount
            self.v.circle_radius_adjust = self.spacing_slider.amount/2.3
            # Update the window
            self.canvas.fill(pygame.Color('black'))

            # self.canvas.blit(surface2, (120, 120))
            for _object in self._object:
                _object.handle_events(events)
            x, y = self.canvas.get_size()
            for _object in self._object:
                _object.draw(x, y)


            pygame.display.update()
            # pygame.display.flip()
            # Clamp FPS
            clock.tick(FPS)
