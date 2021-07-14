import pygame.font


class Button:

    # round edges of button?
    # use button between levels in game?

    def __init__(self, underwater_game, message):
        """Initialize button attributes"""
        self.screen = underwater_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 400, 100
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 52)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message need sto be prepped only once.
        self._prep_message(message)

    def _prep_message(self, message):
        """Turn message into a rendered image and center text on the button."""
        self.message_image = self.font.render(message, True, self.text_color,
                                              self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
