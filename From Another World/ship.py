import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """INITIALIZE THE SHIP AND SET ITS STARTING POSITION"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # LOAD THE SHIP IMAGE AND GET ITS RECT
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # START EACH NEW SHIP AT THE BOTTOM CENTER OF THE SCREEN
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        # MOVEMENT FLAGS
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """UPDATE THE SHIP'S POSITION BASED ON THE MOVEMENT FLAGS"""
        # UPDATE THE SHIP'S CENTER VALUE, NOT THE RECT
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """DRAW THE SHIP AT ITS CURRENT LOCATION"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """CENTER THE SHIP ON THE SCREEN"""
        self.center = self.screen_rect.centerx