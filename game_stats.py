class GameStats:
    """Track statistics for Underwater Game."""

    def __init__(self, underwater_game):
        """Initialize Statistics"""
        self.settings = underwater_game.settings
        self.reset_stats()

        # Launch game inactive so that player will click Play button to begin the game.
        self.game_active = False

        # Prevent the high score from being reset while game is running.
        self.high_score = 0

    def reset_stats(self):
        """Initialize dynamic stats for submarine lives, score and level."""
        self.submarines_left = self.settings.submarine_limit
        self.score = 0
        self.level = 1
