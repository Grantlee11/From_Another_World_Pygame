import pygame
from pygame.sprite import Sprite

class Alien_Bullet(Sprite):
    """A CLASS TO MANAGE BULLETS FIRED FROM THE SHIP"""

    def __init__(self, ai_settings, screen, alien):
        """CREATE A BULLET OBJECT AT THE SHIP'S CURRENT POSITION"""
        super(Alien_Bullet, self).__init__()
        self.screen = screen

        # CREATE A BULLET RECT AT (0, 0) AND THEN SET CORRECT POSITION
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom
        
        # STORE THE BULLET'S POSITION AS A DECIMAL VALUE
        self.y = float(self.rect.y)

        self.color = ai_settings.alien_bullet_color
        self.speed_factor = ai_settings.alien_bullet_speed_factor
    
    def update(self):
        """MOVE THE BULLET DOWN THE SCREEN"""
        # UPDATE THE DECIMAL POSITION OF THE BULLET
        self.y += self.speed_factor
        # UPDATE THE RECT POSITION
        self.rect.y = self.y

    def draw_bullet(self):
        """DRAW THE BULLET TO THE SCREEN"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        