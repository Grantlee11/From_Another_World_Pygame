import pygame
import random
from pygame.sprite import Sprite

class Alien(Sprite):
    """A CLASS TO REPRESENT A SINGLE ALIEN"""

    def __init__(self, ai_settings, screen, image):
        """INITIALIZE THE ALIEN AND SET ITS STARTING POSITION"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # LOAD THE ALIEN IMAGE AND SET ITS RECT ATTRIBUTE
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        # START EACH NEW ALIEN NEAR THE TOP LEFT OF THE SCREEN
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # STORE THE ALIEN'S EXACT POSITION
        self.x = float(self.rect.x)

        self.hp = 1

        self.shoot = random.randint(1, 10)


    def blitme(self):
        """DRAW THE ALIEN AT ITS CURRENT LOCATION"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """RETURN TRUE IF ALIEN IS AT EDGE OF SCREEN"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """MOVE THE ALIEN RIGHT OR LEFT"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.wave_direction)
        self.rect.x = self.x


        