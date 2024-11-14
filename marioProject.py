import sys
import pygame as pg
import random
import math
from pygame import KEYDOWN

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
font = pg.font.Font(None, 40)

# Sounds
coin_sound = pg.mixer.Sound("./coin_sound.wav")
gameover_snd = pg.mixer.Sound('./game_over.wav')
jump_snd = pg.mixer.Sound("./jump_sound.wav")
win_sound = pg.mixer.Sound("./Castle_win.mp3")
background_sound = pg.mixer.Sound("./background_music.mp3")
background_sound.set_volume(0.5)
background_sound.play(loops=-1, maxtime=0)

background = pg.image.load("mario_background.png")
background = pg.transform.scale(background, (800, 600))
background_width = background.get_width()
game_over_background = pg.image.load('maxresdefault.webp')
game_over_background = pg.transform.scale(game_over_background, (800, 600))
win_background = pg.image.load('super-mario-bros-level-ending-1024x576.jpg')
win_background = pg.transform.scale(win_background, (800, 600))
scroll = 0
tiles = math.ceil(800 / background_width) + 1
player_img = pg.image.load("super-mario-bros-mario-kart-8-toad-mario-bros-thumbnail-removebg-preview.png")
player_img = pg.transform.scale(player_img, (50, 50))
player = pg.Rect((100, 459, 50, 50))

block = pg.image.load('block-removebg-preview.png')
block = pg.transform.scale(block, (40, 40))
block_s = []
block_spawn_time = 0
block_interval = 1500

enemy_img = pg.image.load("goomba-removebg-preview.png")
enemy_img = pg.transform.scale(enemy_img, (50, 50))
enemies = []
enemies_spawn_time = 0
enemies_interval = 3000

coin_img = pg.image.load(
    "png-clipart-super-mario-bros-super-mario-land-2-6-golden-coins-8-bit-mario-bros-super-mario-bros-rectangle-removebg-preview.png")
coin_img = pg.transform.scale(coin_img, (30, 30))
coins = []
coin_spawn_time = 0
coin_interval = 2000
powerup1_img = pg.image.load("images-removebg-preview.png")
powerup1_img = pg.transform.scale(powerup1_img, (30, 30))
powerup2_img = pg.image.load("starpowerup-removebg-preview.png")
powerup2_img = pg.transform.scale(powerup2_img, (30, 30))
powerups_2 = []
powerups_2_spawn_time = 0
powerups_2_interval = 5000
powerups = []
powerup_spawn_time = 0
powerup_interval = 4000
powerup2_size_spawn_time = 0
powerup2_size_interval = 5000
powerup_gravity_time = 0
powerup_gravity_interval = 3000
platform = pg.Rect((0, 500, 800, 20))
player_speed_x, player_speed_y = 0, 0
gravity = 0.5
jump = -15
jumping = False
game_over = False
score = 0
win_text = pg.font.Font(None, 50)
instruction_1 = pg.font.Font(None, 35)
instruction_1_render = instruction_1.render('Move Left: a', False, (0, 0, 0))
enemy_direction = 3
score_text = pg.font.Font(None, 35)
instruction_2 = pg.font.Font(None, 35)
instruction_3 = pg.font.Font(None, 35)
instruction_2_render = instruction_2.render('Move Right: d', False, (0, 0, 0))
instruction_3_render = instruction_3.render('Jump: SPACEBAR', False, (0, 0, 0))
win_instruction = pg.font.Font(None, 47)
win_instruction_render = win_instruction.render('Restart: Press r', False, (255, 255, 255))
quit_text = pg.font.Font(None, 35)
quit_text_render = quit_text.render('Quit: q', False, (0, 0, 0))

game_over_time = None
win_sound_played = False

while True:
    screen.blit(background, (0, 0))

    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE] or keys[pg.K_q]:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not jumping and not game_over:
            player_speed_y = jump
            jumping = True
            jump_snd.play()

        if game_over:
            if event.type == KEYDOWN and event.key == pg.K_r:
                game_over = False
                game_over_time = None
                player_img = pg.transform.scale(player_img, (50, 50))
                score = 0
                coins = []
                block_s = []
                powerups = []
                powerups_2 = []
                player_speed_y = 0
                player_speed_x = 0
                jumping = False
                enemies = []
                background_sound.play(loops=-1, maxtime=0)

    for i in range(0, tiles):
        screen.blit(background, (i * background_width + scroll, 0))
        scroll -= 2

    if abs(scroll) > background_width:
        scroll = 0

    current_time = pg.time.get_ticks()

    if current_time - block_spawn_time > block_interval:
        block_blit_x = random.randint(1, 600)
        block_blit_y = random.randint(250, 350)
        next_block = pg.Rect(block_blit_x, block_blit_y, 50, 50)
        block_s.append(next_block)
        block_spawn_time = current_time

    if current_time - powerup_spawn_time > powerup_interval:
        powerup_blit_x = random.randint(50, 750)
        powerup_blit_y = random.randint(100, 459)
        power_rect = pg.Rect((powerup_blit_x, powerup_blit_y, 30, 30))
        powerups.append(power_rect)
        powerup_spawn_time = current_time

    if current_time - coin_spawn_time > coin_interval:
        coin_blit_x = random.randint(50, 750)
        coin_blit_y = random.randint(100, 459)
        coin_rect = pg.Rect((coin_blit_x, coin_blit_y, 30, 30))
        coins.append(coin_rect)
        coin_spawn_time = current_time

    if current_time - enemies_spawn_time > enemies_interval:
        enemies_blit_y = 459
        enemies_blit_x = random.randint(50, 750)
        enemies_rect = pg.Rect((enemies_blit_x, enemies_blit_y, 50, 50))
        enemies.append(enemies_rect)
        enemies_spawn_time = current_time

    if current_time - powerups_2_spawn_time > powerups_2_interval:
        powerup2_blit_x = random.randint(50, 750)
        powerup2_blit_y = random.randint(100, 459)
        powerups2_rect = pg.Rect((powerup2_blit_x, powerup2_blit_y, 30, 30))
        powerups_2.append(powerups2_rect)
        powerups_2_spawn_time = current_time

    for b in block_s:
        b.y += gravity
        if b.y > 450:
            block_s.remove(b)

    if not game_over:
        if keys[pg.K_d]:
            player_speed_x = 5
        elif keys[pg.K_a]:
            player_speed_x = -5
        else:
            player_speed_x = 0

        if player.x > 750:
            player_speed_x = -5
        if player.x < 0:
            player_speed_x = 5

        player_speed_y += gravity
        player.x += player_speed_x
        player.y += player_speed_y

        if player.colliderect(platform) and player_speed_y > 0:
            player.y = platform.y - player.height
            player_speed_y = 0
            jumping = False

        for b in block_s:
            if player.colliderect(b) and player_speed_y > 0:
                player.y = b.y - player.height
                player_speed_y = 0
                jumping = False

        for enemy in enemies:
            enemy.x += enemy_direction
            if enemy.x > 750 or enemy.x < 0:
                enemy_direction *= -1
            if player.colliderect(enemy):
                game_over = True
                game_over_time = current_time
                gameover_snd.play()
                background_sound.stop()

        for coin in coins:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 100
                coin_sound.play()

        for powerup in powerups:
            if player.colliderect(powerup):
                powerups.remove(powerup)
                gravity = 0.3
                powerup_gravity_time = current_time

        if current_time - powerup_gravity_time > powerup_gravity_interval:
            gravity = 0.5

        for powerup2 in powerups_2:
            if player.colliderect(powerup2):
                powerups_2.remove(powerup2)
                player_img = pg.transform.scale(player_img, (70, 70))
                powerup2_size_spawn_time = current_time

        if current_time - powerup2_size_spawn_time > powerup2_size_interval:
            player_img = pg.transform.scale(player_img, (50, 50))

        screen.blit(player_img, player.topleft)

        for b in block_s:
            screen.blit(block, b.topleft)

        pg.draw.rect(screen, (0, 255, 0), platform)

        for enemy in enemies:
            screen.blit(enemy_img, enemy.topleft)
        for coin in coins:
            screen.blit(coin_img, coin.topleft)
        for powerup in powerups:
            screen.blit(powerup1_img, powerup.topleft)
        for powerup2 in powerups_2:
            screen.blit(powerup2_img, powerup2.topleft)

        score_text_render = score_text.render(f'Score: {score}', False, (0, 0, 0))
        screen.blit(score_text_render, (10, 10))
        screen.blit(instruction_1_render, (10, 40))
        screen.blit(instruction_2_render, (10, 70))
        screen.blit(instruction_3_render, (10, 100))
        screen.blit(quit_text_render, (10, 130))


    else:
        screen.blit(game_over_background, (0, 0))
        if game_over_time:
            till_game_over = current_time - game_over_time
            if till_game_over > 5000:
                pass

    if score == 500:
        background_sound.stop()
        screen.blit(win_background, (0, 0))
        win_text_rendered = win_text.render("YOU WIN", False, (255, 255, 255))
        win_rect = win_text_rendered.get_rect(center=(400, 300))
        win_background.blit(win_text_rendered, win_rect)
        win_background.blit(win_instruction_render, (280, 320))
        if not win_sound_played:
            win_sound.play()
            win_sound_played = True
        game_over = True

    clock.tick(60)
    pg.display.flip()