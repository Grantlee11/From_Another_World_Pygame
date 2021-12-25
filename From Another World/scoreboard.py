import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """A CLASS TO REPORT SCORING INFORMATION"""

    def __init__(self, ai_settings, screen, stats):
        """INITIALIZE SCOREKEEPING ATTRIBUTES"""
        self.screen = screen

        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # FONT SETTINGS FOR SCORING INFORMATION
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # PREPARE THE INITIAL SCORE IMAGES
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """TURN THE SCORE INTO A RENDERED IMAGE"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # DISPLAY THE SCORE AT THE TOP RIGHT OF THE SCREEN
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = 10

    def show_score(self):
        """DRAW SCORES AND SHIPS TO THE SCREEN"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


    def prep_level(self):
        """TURN THE LEVEL INTO A RENDERED IMAGE"""
        self.level_image = self.font.render(("LEVEL " + str(self.stats.level)), True, self.text_color, self.ai_settings.bg_color)
        # POSITIONS THE LEVEL
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 10
        self.level_rect.top = 10

    def prep_ships(self):
        """SHOW HOW MANY SHIPS ARE LEFT"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)