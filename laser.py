import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    """A class to manage lasers fired from the submarine"""

    def __init__(self, underwater_game):
        """Create a laser object at the submarine's current position."""
        super().__init__()
        self.screen = underwater_game.screen
        self.settings = underwater_game.settings
        self.color = self.settings.laser_color

        # Create a laser rect at (0,0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.laser_width,
                                self.settings.laser_height)
        self.rect.midright = underwater_game.submarine.rect.midright

        # Store the laser's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move laser from left to right across the screen."""
        # Update the decimal position of the laser.
        self.x += self.settings.blast_speed
        # Update the rect position
        self.rect.x = self.x

    def draw_laser(self):
        """Draw the laser on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
