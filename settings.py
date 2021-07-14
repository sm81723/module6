class Settings:
    """A class to store all settings for Underwater Game."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 120)

        # todo can't get this working... also current background image width is 2400
        # Scrolling Screen
        self.world_width = 2400

        # Submarine Settings
        self.submarine_limit = 4

        # Laser Settings
        self.laser_width = 10
        self.laser_height = 10
        self.laser_color = (230, 0, 0)
        self.blasts_allowed = 100

        # Game acceleration when player levels up.
        self.speedup_scale = 1.3

        # Point multiplier when player levels up.
        self.score_scale = 2.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.submarine_speed = 10
        self.blast_speed = 14

        # Whale Settings
        self.whale_speed = 12
        self.whale_frequency = 0.05

        # Shark Settings
        self.shark_speed = 20
        self.shark_frequency = 0.008

        # Jellyfish Settings
        self.jellyfish_speed = 6
        self.jellyfish_frequency = 0.08

        # Scoring
        self.whale_points = 50
        self.shark_points = 100
        self.jellyfish_points = 25

    def increase_difficulty(self):
        """Apply dynamic settings to increase speed and point multiplier when player levels up."""
        self.submarine_speed *= self.speedup_scale
        self.blast_speed *= self.speedup_scale

        self.whale_speed *= self.speedup_scale
        self.whale_frequency *= self.speedup_scale
        self.whale_points = int(self.whale_points * self.score_scale)

        self.shark_speed *= self.speedup_scale
        self.shark_frequency *= self.speedup_scale
        self.shark_points = int(self.shark_points * self.score_scale)

        self.jellyfish_speed *= self.speedup_scale
        self.jellyfish_frequency *= self.speedup_scale
        self.jellyfish_points = int(self.jellyfish_points * self.score_scale)
