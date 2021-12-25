class Settings():
    """A CLASS TO STORE ALL SETTINGS FOR THE ALIEN SHOOTER"""

    def __init__(self):
        """INITIALIZE THE GAME'S STATIC SETTINGS"""
        # SCREEN SETTINGS
        self.screen_width =  1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # SHIP SETTINGS
        self.ship_limit = 3

        # SHIP BULLET SETTINGS
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 100, 100, 100
        self.bullets_allowed = 5

        # ALIEN BULLET SETTINGS
        self.alien_bullet_speed_factor = 0.4
        self.alien_bullet_width = 3
        self.alien_bullet_height = 10
        self.alien_bullet_color = 255, 255, 255

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """INITIALIZE SETTINGS THAT CHANGE THROUGHOUT THE GAME"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.2
        self.wave_drop_speed = 5
        self.wave_direction = 1

        # SCORING
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor += 0.1
        self.bullet_speed_factor += 0.2
        self.alien_speed_factor += 0.025
        self.wave_drop_speed += 0.5
        self.alien_points += 25