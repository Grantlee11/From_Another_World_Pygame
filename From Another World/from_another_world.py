import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame import mixer
import game_functions as  gf
  
def run_game():
    # INITIALIZE PYGAME, SETTINGS, AND SCREEN OBJECT
    pygame.init()
    ai_settings = Settings() 
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("FROM ANOTHER WORLD")

    # OPENING SCREEN
    play_button = Button(screen, "CLICK TO FIGHT ALIENS")

    mixer.music.load('Tours-Enthusiast.mp3')
    mixer.music.set_volume(0.15)
    mixer.music.play(-1)

    # CREATE AN INSTANCE TO STORE GAME STATISTICS AND CREATE A SCOREBOARD
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
  
    # CREATES A SHIP, AND GROUPS OF BULLETS, ALIENS, AND ALIEN_BULLETS
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    alien_bullets = Group()


    # START THE MAIN LOOP FOR THE GAME
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
            gf.update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alien_bullets)

run_game()