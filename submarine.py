import pygame
from pygame.sprite import Sprite


class Submarine(Sprite):
    """Class to manage player controlled submarine."""

    def __init__(self, underwater_game):
        """Initialize the submarine and set its starting position."""
        super().__init__()
        self.screen = underwater_game.screen
        self.settings = underwater_game.settings
        self.screen_rect = underwater_game.screen.get_rect()

        # Load the submarine image and get its rect.
        self.image = pygame.image.load('images/submarine.bmp')
        self.rect = self.image.get_rect()

        # Start the submarine in the middle of the left edge of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store the horizontal and vertical decimal positions of the submarine.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the submarine's position based on the movement flags."""
        # todo this likely should be altered for the scrolling screen.

        # Update the submarine's x and y values, not the rect.
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.submarine_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.submarine_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.submarine_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.submarine_speed

        # update rect object from self.y.
        self.rect.y = self.y
        self.rect.x = self.x

    def blitme(self):
        """Draw the submarine at its current location."""
        self.screen.blit(self.image, self.rect)
