import sys
from random import random
from time import sleep

import pygame
from pygame.sprite import Group, Sprite
from pygame.time import Clock

from button import Button
from game_stats import GameStats
from jellyfish import Jellyfish
from laser import Laser
from scoreboard import Scoreboard
from settings import Settings
from shark import Shark
from submarine import Submarine
from whale import Whale


# todo need to add horizontal scrolling
# todo need to use setup.py
# todo improve level transition?


class Background(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.settings = Settings()
        self.image = pygame.image.load("images/seabackground.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = self.settings.screen_height


class Viewport:
    def __init__(self):
        self.left = 0


class UnderwaterGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        pygame.display.set_caption("Underwater Game")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.submarine = Submarine(self)
        self.lasers = pygame.sprite.Group()
        self.whales = pygame.sprite.Group()
        self.sharks = pygame.sprite.Group()
        self.jellyfishes = pygame.sprite.Group()

        self.static_sprites = Group()
        self.static_sprites.add(Background())
        self.viewport = Viewport

        self.play_button = Button(self, "Play")

    def run_game(self):
        """Game Loop"""
        clock = Clock()

        while True:
            self._check_events()

            self._create_whale()
            self._create_shark()
            self._create_jellyfish()

            if self.stats.game_active:
                self.submarine.update()
                self._update_lasers()
                # self.sea_creatures.update()
                # self._update_sea_creatures()
                self._update_whales()
                self._update_sharks()
                self._update_jellyfishes()

            self._update_screen()

            clock.tick(30)

    def _update_lasers(self):
        self.lasers.update()

        # Removes laser blasts that have disappeared.
        for laser in self.lasers.copy():
            if laser.rect.left >= self.screen.get_rect().right:
                self.lasers.remove(laser)

        self._check_laser_creature_collisions()

    def _check_laser_creature_collisions(self):
        # Collision detection for lasers and sea creatures.
        # Removes laser and sea creature when contact is made.

        whales_collisions = pygame.sprite.groupcollide(
            self.lasers, self.whales, True, True
        )

        sharks_collisions = pygame.sprite.groupcollide(
            self.lasers, self.sharks, True, True
        )

        jellyfishes_collisions = pygame.sprite.groupcollide(
            self.lasers, self.jellyfishes, True, True
        )

        if whales_collisions:
            for whales in whales_collisions.values():
                self.stats.score += self.settings.whale_points
            self.update_difficulty_and_score()

        if sharks_collisions:
            for sharks in sharks_collisions.values():
                self.stats.score += self.settings.shark_points
            self.update_difficulty_and_score()

        if jellyfishes_collisions:
            for jellyfishes in jellyfishes_collisions.values():
                self.stats.score += self.settings.jellyfish_points
            self.update_difficulty_and_score()

    def update_difficulty_and_score(self):
        self.sb.prep_score()
        self.sb.check_high_score()

        if self.stats.score == 1000:
            self.settings.increase_difficulty()
            self.stats.level += 1
            self.sb.prep_level()
            self._update_screen()
            sleep(0.5)

        if self.stats.score == 2500:
            self.settings.increase_difficulty()
            self.stats.level += 1
            self.sb.prep_level()
            sleep(0.5)

        if self.stats.score == 7500:
            self.settings.increase_difficulty()
            self.stats.level += 1
            self.sb.prep_level()
            sleep(0.5)

        if self.stats.score == 10000:
            self.settings.increase_difficulty()
            self.stats.level += 1
            self.sb.prep_level()
            sleep(0.5)

    def _update_whales(self):
        self.whales.update()

        # Look for whale-submarine collisions.
        if pygame.sprite.spritecollideany(self.submarine, self.whales):
            self._submarine_hit()

    def _update_sharks(self):
        self.sharks.update()

        # Look for shark-submarine collisions.
        if pygame.sprite.spritecollideany(self.submarine, self.sharks):
            self._submarine_hit()

    def _update_jellyfishes(self):
        self.jellyfishes.update()

        # Look for jellyfish-submarine collisions.
        if pygame.sprite.spritecollideany(self.submarine, self.jellyfishes):
            self._submarine_hit()

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.static_sprites.draw(self.screen)
        self.submarine.blitme()

        for laser in self.lasers.sprites():
            laser.draw_laser()

        self.whales.draw(self.screen)
        self.sharks.draw(self.screen)
        self.jellyfishes.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_events(self):
        # Check for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.submarine.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.submarine.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.submarine.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.submarine.moving_left = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            self.submarine.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.submarine.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.submarine.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.submarine.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_laser()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the Play button is clicked."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_submarines()

            # Remove the remaining sea_creatures and lasers.
            self.whales.empty()
            self.sharks.empty()
            self.jellyfishes.empty()
            self.lasers.empty()

            # Create sea creatures when game is started.
            self._create_whale()
            self._create_shark()
            self._create_jellyfish()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _fire_laser(self):
        """Create a new laser and add it to the lasers group."""
        if len(self.lasers) < self.settings.blasts_allowed:
            new_laser = Laser(self)
            self.lasers.add(new_laser)

    def _create_whale(self):
        if random() < self.settings.whale_frequency:
            whale = Whale(self)
            self.whales.add(whale)

    def _create_shark(self):
        if random() < self.settings.shark_frequency:
            shark = Shark(self)
            self.sharks.add(shark)

    def _create_jellyfish(self):
        if random() < self.settings.jellyfish_frequency:
            jellyfish = Jellyfish(self)
            self.jellyfishes.add(jellyfish)

    def _submarine_hit(self):
        """Respond to the submarine being hit by a sea creature."""
        if self.stats.submarines_left > 0:
            # Decrement submarines_left, and update scoreboard.
            self.stats.submarines_left -= 1
            self.sb.prep_submarines()

            # Remove the remaining sea_creatures and lasers.
            self.whales.empty()
            self.sharks.empty()
            self.jellyfishes.empty()
            self.lasers.empty()

            # Create sea creature enemies
            self._create_whale()
            self._create_shark()
            self._create_jellyfish()

            # Brief pause when a submarine is hit by a sea creature
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


if __name__ == '__main__':
    # Create instance of UnderwaterGame and launch it.
    uw_game = UnderwaterGame()
    uw_game.run_game()
