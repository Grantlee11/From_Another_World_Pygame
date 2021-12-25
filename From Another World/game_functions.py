import sys
import pygame
import random
from bullet import Bullet
from alien_bullet import Alien_Bullet
from alien import Alien
from textbox import TextBox
from pygame import mixer
from time import sleep


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets):
    """RESPOND TO KEYPRESSES AND MOUSE CLICKS"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, alien_bullets)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, alien_bullets):
    """STARTS GAME WHEN "CLICK TO FIGHT ALIENS" BUTTON IS CLICKED"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # RESETS GAME STATS AND SETTINGS
        ai_settings.initialize_dynamic_settings()

        # HIDES THE MOUSE CURSOR
        pygame.mouse.set_visible(False)

        # RESETS THE GAME STATS AND MAKES THE GAME ACTIVE
        stats.reset_stats()
        stats.game_active = True

        # RESETS ALL SCOREBOARD IMAGES
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        # GETS RID OF ALIENS AND ALL BULLETS ON THE SCREEN
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

        # CREATES FIRST WAVE OF ENEMY ALIENS
        if stats.level == 10:
            create_boss(ai_settings, screen, aliens)
        elif stats.level % 3 == 0:
            create_mini_boss_wave(ai_settings, screen, aliens, stats)
        else:
            create_wave(ai_settings, screen, ship, aliens)
        ship.center_ship()            

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats):
    """PROGRESSES GAME ACCORDING TO KEYPRESS"""
    if stats.game_active:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

def check_keyup_events(event, ship):
    """CHANGES MOVEMENT FLAG WHEN KEY IS RELEASED"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def fire_bullet(ai_settings, screen, ship, bullets):
    """FIRE A BULLET IF LIMIT NOT REACHED YET"""
    # CREATES NEW BULLETS AS LONG AS CURRENT LIMIT ISNT REACHED
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        bullet_sound_generator()

def bullet_sound_generator():
    """CREATES THE BULLET SOUND"""
    bullet_sound = mixer.Sound('LaserShot.mp3')
    bullet_sound.set_volume(0.6)
    bullet_sound.play()

def fire_alien_bullet(ai_settings, screen, alien_bullets, alien, stats):
    """CREATES INSTANCE OF ALIEN BULLET AND ADDS IT TO GROUP"""
    new_bullet = Alien_Bullet(ai_settings, screen, alien)
    # IF ON FINAL LEVEL, GIVE MOTHERSHUP NEW ATTACKING SPOTS
    if stats.level == 10:
        x = random.randint(1, 5)
        if x == 1:
            new_bullet.rect.centerx = alien.rect.left + 10
        elif x == 2:
            new_bullet.rect.centerx = alien.rect.right - 10
    alien_bullets.add(new_bullet)

def update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets):
    """UPDATES ALIEN BULLET POSITION AND REMOVES IT FROM SCREEN WHEN NEEDED"""
    alien_bullets.update()

    # IF BULLET IS BELOW SCREEN REMOVE IT
    for bullet in alien_bullets.copy():
        if bullet.rect.top >= 800:
            alien_bullets.remove(bullet)
    
    check_ship_bullet_collision(ai_settings, screen, stats, sb, ship, alien_bullets, aliens, bullets)

def check_ship_bullet_collision(ai_settings, screen, stats, sb, ship, alien_bullets, aliens, bullets):
    """CHECKS IF AN ALIEN BULLET HITS THE SHIP, IF SO RESTART LEVEL"""
    collision = pygame.sprite.spritecollide(ship, alien_bullets, True)
    if collision:
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    """UPDATES BULLET POSITION AND REMOVES IT FROM SCREEN WHEN NEEDED"""
    bullets.update()

    # IF BULLET IS ABOVE SCREEN REMOVE IT
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

def alien_explosion_sound():
    alien_explosion = mixer.Sound('Explosion.wav')
    alien_explosion.set_volume(0.25)
    alien_explosion.play()

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    """PROCESSES ALIEN AND BULLET COLLISIONS"""

    # IF ALIEN COLLIDES WITH BULLET AND ALIEN HP IS TOO LOW, KILL ALIEN
    # OTHERWISE LOWER ALIEN HP
    for alien in aliens:
        collision = pygame.sprite.spritecollide(alien, bullets, True)
        if collision:
            alien.hp -= 1
            alien_explosion_sound()
            if alien.hp < 1:
                stats.score += ai_settings.alien_points
                sb.prep_score()
                alien.kill()

    # IF ALIENS LEFT EQUALS ZERO START NEW LEVEL
    if len(aliens) == 0:
    
        # AFTER 10 LEVELS, END THE GAME
        if stats.level < 10:

            bullets.empty()
            alien_bullets.empty()
            ai_settings.increase_speed()
            
            stats.level += 1
            sb.prep_level()

            sleep(0.25)

            # CREATE WAVE OR BOSS DEPENDING ON LEVEL
            if stats.level == 10:
                create_boss(ai_settings, screen, aliens)
            elif stats.level % 3 == 0:
                create_mini_boss_wave(ai_settings, screen, aliens, stats)
            else:
                create_wave(ai_settings, screen, ship, aliens)
        elif stats.level == 10:
            stats.level += 1
            stats.game_active = False
            sleep(0.2)


def create_mini_boss_wave(ai_settings, screen, aliens, stats):
    """CONTROLS AMOUNT OF MINI BOSSES CREATED PER LEVEL"""
    if stats.level == 3:
        create_mini_boss_level_3(ai_settings, screen, aliens)
    elif stats.level == 6:
        create_mini_boss_level_6(ai_settings, screen, aliens)
    elif stats.level == 9:
        create_mini_boss_level_9(ai_settings, screen, aliens)

def create_mini_boss_level_3(ai_settings, screen, aliens):
    """CREATES LEVEL 3 MINI BOSS"""
    image = 'images/commandership.bmp'
    alien = Alien(ai_settings, screen, image)

    alien.hp = 25

    alien.x = 1

    alien.rect.x = alien.x

    alien.rect.y = 100

    aliens.add(alien)

def create_mini_boss_level_6(ai_settings, screen, aliens):
    """CREATES LEVEL 6 MINI BOSSES"""
    image = 'images/commandership.bmp'
    alien1 = Alien(ai_settings, screen, image)
    alien2 = Alien(ai_settings, screen, image)

    alien1.hp = 25
    alien2.hp = 25

    alien1.x = 1
    alien2.x = 500

    alien1.rect.x = alien1.x
    alien2.rect.x = alien2.x

    alien1.rect.y = 100
    alien2.rect.y = alien1.rect.y
    
    aliens.add(alien1)
    aliens.add(alien2)

def create_mini_boss_level_9(ai_settings, screen, aliens):
    """CREATES LEVEL 9 MINI BOSSES"""
    image = 'images/commandership.bmp'
    alien1 = Alien(ai_settings, screen, image)
    alien2 = Alien(ai_settings, screen, image)
    alien3 = Alien(ai_settings, screen, image)

    alien1.hp = 25
    alien2.hp = 25
    alien3.hp = 25

    alien1.x = 1
    alien2.x = 500
    alien3.x = 250

    alien1.rect.x = alien1.x
    alien2.rect.x = alien2.x
    alien3.rect.x = alien3.x
    
    alien1.rect.y = 100
    alien2.rect.y = alien1.rect.y
    alien3.rect.y = 300
    
    aliens.add(alien1)
    aliens.add(alien2)
    aliens.add(alien3)

def create_boss(ai_settings, screen, aliens):
    """CREATES THE MOTHERSHIP"""
    image = 'images/MotherShip.bmp'
    alien = Alien(ai_settings, screen, image)
    ai_settings.alien_speed_factor = 1.2
    alien.hp = 75
    alien.x = 1
    alien.rect.x = alien.x
    alien.rect.y = 100
    aliens.add(alien)

def get_number_aliens_x(ai_settings, alien_width):
    """DETERMINE THE NUMBER OF ALIENS THAT FIT IN A ROW"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """DETERMINE THE NUMBER OF ROWS OF ALIENS THAT FIT ON THE SCREEN"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """CREATE AN ALIEN AND PLACE IT NEXT IN LINE"""
    image = 'images/SingleAlienShip.bmp'
    alien = Alien(ai_settings, screen, image)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = (alien.rect.height + 2 * alien.rect.height * row_number) + 20
    aliens.add(alien)

def create_wave(ai_settings, screen, ship, aliens):
    """CREATE WAVE OF ALIENS"""
    # CHECK HOW MANY ALIENS FIT TO SCREEN
    image = 'images/SingleAlienShip.bmp'
    alien = Alien(ai_settings, screen, image)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # CREATE WAVE OF ALIENS
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_wave_edges(ai_settings, aliens):
    """CHECK AND SEE IF AN ALIEN REACHED EDGE, THEN CHANGE WAVE DIRECTION"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_wave_direction(ai_settings, aliens)
            break

def change_wave_direction(ai_settings, aliens):
    """DROP THE WAVE AND CHANGE WAVE'S DIRECTION"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.wave_drop_speed
    ai_settings.wave_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets):
    """PROCESSES SHIP BEING HIT BY ALIEN, ALIEN BULLET, OR ALIEN REACHING BOTTOM"""
    # IF A SHIP IS LEFT, RESTART THE LEVEL, ELSE, RESTART GAME
    if stats.ships_left > 0:
        
        stats.ships_left -= 1
        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

        # RESTART THE CURRENT LEVEL
        if stats.level == 10:
            create_boss(ai_settings, screen, aliens)
        elif stats.level % 3 ==0:
            create_mini_boss_wave(ai_settings, screen, aliens, stats)
        else:
            create_wave(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # PAUSE
        sleep(0.5)
    else:
        sleep(0.5)
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets):
    """CHECK IF AN ALIEN HAS REACHED THE BOTTOM OF THE SCREEN"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # TREAT THIS THE SAME AS IF THE SHIP GOT HIT
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets):
    """PROCESSES ALIENS MOVEMENT AND BULLET FIRING POSITIONS"""
    check_wave_edges(ai_settings, aliens)
    aliens.update()

    # DEPENDING ON LEVEL, UPDATE ALIEN FIRING RATE
    if stats.level == 10:
        for alien in aliens:
                if random.randint(0, 400) == 200:
                    fire_alien_bullet(ai_settings, screen, alien_bullets, alien, stats)
    elif stats.level % 3 == 0:
        for alien in aliens:
            if random.randint(0, 1000) == 500:
                fire_alien_bullet(ai_settings, screen, alien_bullets, alien, stats)
    else:
        for alien in aliens:
            if random.randint(0, 5000) == 750:
                fire_alien_bullet(ai_settings, screen, alien_bullets, alien, stats)

    # CHECK FOR ALIEN AND SHIP COLLIDING
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)

    # CHECK FOR ALIENS HITTING THE BOTTOM OF SCREEN
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)

def end_seq(screen, stats):
    """CREATES THE GAMES ENDING SCREEN"""

    end_screen1 = TextBox(screen, "Your Score: " + str(stats.score + (10000 * (stats.ships_left + 1))), 0)
    end_screen1.draw_button()

    end_screen2 = TextBox(screen, "", 80)
    end_screen2.draw_button()

    end_screen3 = TextBox(screen, "CREDITS:", 160)
    end_screen3.draw_button()

    end_screen4 = TextBox(screen, "BACKGROUND MUSIC:", 240)
    end_screen4.draw_button()

    end_screen5 = TextBox(screen, "Enthusiast by Tours | https://freemusicarchive.org/music/Tours", 320)
    end_screen5.draw_button()

    end_screen6 = TextBox(screen, "Music promoted by https://www.chosic.com/free-music/all/", 400)
    end_screen6.draw_button()

    end_screen7 = TextBox(screen, "Creative Commons CC BY 3.0", 480)
    end_screen7.draw_button()

    end_screen8 = TextBox(screen, "https://creativecommons.org/licenses/by/3.0/", 560)
    end_screen8.draw_button()

    end_screen9 = TextBox(screen, "", 640)
    end_screen9.draw_button()

    end_screen10 = TextBox(screen, "VISUAL ART AND GAME DESIGN BY GRANT LEE", 720)
    end_screen10.draw_button()

def begin_seq(screen):
    start_screen1 = TextBox(screen, "CAPTAIN, A HOSTILE ALIEN FORCE", 0)
    start_screen1.draw_button()

    start_screen1 = TextBox(screen, "WAS JUST SPOTTED ENTERING OUR SOLAR", 80)
    start_screen1.draw_button()

    start_screen1 = TextBox(screen, "SYSTEM. YOUR CREW IS ALL WE CAN SPARE", 160)
    start_screen1.draw_button()

    start_screen1 = TextBox(screen, "TO TAKE ON THIS ALIEN THREAT.", 240)
    start_screen1.draw_button()

    start_screen1 = TextBox(screen, "GOOD LUCK.", 320)
    start_screen1.draw_button()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alien_bullets):
    """UPDATE IMAGES ON THE SCREEN AND FLIP TO THE NEW SCREEN"""
    # REDRAW THE SCREEN DURING EACH PASS THROUGH THE LOOP
    screen.fill(ai_settings.bg_color)
    # REDRAW ALL BULLETS BEHIND SHIP AND ALIENS
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    
    for bullet in alien_bullets.sprites():
        bullet.draw_bullet()
    
    aliens.draw(screen)

    # DRAW THE SCORE INFORMATION
    sb.show_score()

    # DRAW THE PLAY BUTTON IF THE GAME IS INACTIVE
    if not stats.game_active and stats.level <= 10:
        begin_seq(screen)
        play_button.draw_button()
    elif stats.level > 10:
        end_seq(screen, stats)

    # MAKE THE MOST RECENTLY DRAWN SCREEN VISIBILE
    pygame.display.flip()
