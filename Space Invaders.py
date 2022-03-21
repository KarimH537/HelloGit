import math
import pygame
import random
from pygame import mixer

pygame.init()

# window size and background
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('space_background.png')

# background (sound)
mixer.music.load('background.wav')
mixer.music.play(-1)

# set title
pygame.display.set_caption('Space Invaders')


# set spaceship and coordinates
player_img = pygame.image.load('spaceship.png')
playerX = 380
playerY = 480
player_x_move = 0

# setting chicken
chicken_img = pygame.image.load('chicken.png')
chickenX = random.randint(0, 800)  # random place
chickenY = random.randint(50, 150)
chicken_x_move = 1.5
chicken_y_move = 40

# set bullet
bullet_img = pygame.image.load('laser.png')
bulletX = 0
bulletY = 480
bullet_x_move = 0
bullet_y_move = 4
bullet_state = 'Ready'  # Ready -> not shown  # Fire -> bullet moving

# display score
score_value = 0
font = pygame.font.Font('Race sport.ttf', 28)
scoreX = 10
scoreY = 10


def show_score(x, y):
    score = font.render('Kills : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# display win message
win_font = pygame.font.Font('Race sport.ttf', 64)
winX = 220
winY = 250
win_flag = True


def winner(x, y):
    win = win_font.render('WINNER', True, (255, 0, 255))
    screen.blit(win, (x, y))





def collide(chickenX, chickenY, bulletX, bulletY):
    distance = math.sqrt((math.pow(chickenY - bulletY, 2)) + (math.pow(chickenX - bulletX, 2)))
    if distance < 40:
        return True
    else:
        return False


def chicken(x, y):
    screen.blit(chicken_img, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))  # blit draws the player 'spaceship'


def fire(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bullet_img, (x + 16, y + 10))


window = True
while window:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # game loop that ends when (x) is pressed
            window = False
        if event.type == pygame.KEYDOWN:  # check if key is pressed
            if event.key == pygame.K_LEFT:
                player_x_move = -3.5
            if event.key == pygame.K_RIGHT:
                player_x_move = 3.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":  # get spaceship's place only when ready
                    # bullet sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Reload
                    bulletX = playerX
                    fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_move = 0

    screen.blit(background, (0, 0))

    # player's boundaries
    playerX += player_x_move
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # chicken's movement and boundaries
    chickenX += chicken_x_move
    if chickenX < 0:
        chicken_x_move = 0.3
        chickenY += chicken_y_move
    elif chickenX > 736:
        chicken_x_move = -0.3
        chickenY += chicken_y_move



    # keep bullet moving and reload
    if bulletY < 0:
        bulletY = 480
        bullet_state = "Ready"
    if bullet_state == "Fire":
        fire(bulletX, bulletY)
        bulletY -= bullet_y_move

    # Collision
    collision = collide(chickenX, chickenY, bulletX, bulletY)
    if collision:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        bulletY = 480
        bullet_state = "Ready"
        score_value += 1
        chickenX = random.randint(1, 735)
        chickenY = random.randint(50, 150)

    if score_value == 5:
        if win_flag:
            win_sound = mixer.Sound('fatality.mp3')
            win_sound.play()
        winner(winX, winY)
        chickenY = 2000
        gayarY = 2000
        win_flag = False


    player(playerX, playerY)
    chicken(chickenX, chickenY)
    show_score(scoreX, scoreY)
    pygame.display.update()
