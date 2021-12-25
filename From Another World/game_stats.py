class GameStats():
    """TRACK STATISTICS FOR FROM ANOTHER WORLD"""

    def __init__(self, ai_settings):
        """INITIALIZE STATISTICS"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # START GAME IN AN INACTIVE STATE
        self.game_active = False


    def reset_stats(self):
        """INITIALIZE STATISTICS THAT CAN CHANGE DURING THE GAME"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
