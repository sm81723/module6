import pygame.font
from pygame.sprite import Group

from submarine import Submarine


class Scoreboard:
    """Class that contains score information."""

    def __init__(self, underwater_game):
        """Initialize score-keeping attributes."""
        self.underwater_game = underwater_game
        self.screen = underwater_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = underwater_game.settings
        self.stats = underwater_game.stats

        # Font settings for scoring information.
        self.text_color = (250, 0, 250)
        self.font = pygame.font.SysFont(None, 36)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_submarines()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw scores, level, and submarines to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.submarines.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score_str = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there is a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(f"Level: {self.stats.level}")
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_submarines(self):
        """Show how many submarines are left."""
        self.submarines = Group()
        for submarine_number in range(self.stats.submarines_left):
            submarine = Submarine(self.underwater_game)
            submarine.rect.x = 10 + submarine_number * submarine.rect.width
            submarine.rect.y = 10
            self.submarines.add(submarine)
