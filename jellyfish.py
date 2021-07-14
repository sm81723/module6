from random import randint

import pygame
from pygame.sprite import Sprite


class Jellyfish(Sprite):
    """Class that represents a jellyfish enemy."""

    def __init__(self, underwater_game):
        """Initialize the jellyfish and set its starting position."""
        super().__init__()
        self.screen = underwater_game.screen
        self.settings = underwater_game.settings

        # Load the jellyfish image and sets its rect attribute.
        self.image = pygame.image.load('images/jellyfish.png')
        self.rect = self.image.get_rect()

        # Create each jellyfish at a random position on the right edge of the screen.
        self.rect.left = self.screen.get_rect().right

        # Height of screen - height of jellyfish
        jellyfish_top_max = self.settings.screen_height - self.rect.height
        self.rect.top = randint(0, jellyfish_top_max)

        # Store the horizontal position of the whale.
        self.x = float(self.rect.x)

    def update(self):
        """Move the shark across the screen from right to left."""
        self.x -= self.settings.jellyfish_speed
        self.rect.x = self.x
