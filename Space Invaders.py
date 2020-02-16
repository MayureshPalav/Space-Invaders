import pygame
import random
import math
from pygame import mixer

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load("background.png")
# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player

playerimg = pygame.image.load("player.png")
playerX = 370
playerY = 450
player_change = 0
# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 720))
    enemyY.append(random.randint(50, 150))
    enemyx_change.append(4)
    enemyy_change.append(30)

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletx_change = 0
bullety_change = 10
bullet_state = 'ready'

score_value = 0
over_font = pygame.font.Font('freesansbold.ttf', 64)
font = pygame.font.Font('freesansbold.ttf', 30)
testX = 10
textY = 10


def score(x, y):
    total_score = font.render("score:" + str(score_value), True, (255, 255, 255))
    screen.blit(total_score, (x, y))


def game_over_text():
    game_over = over_font.render("GAME OVER!!!!!", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


def player(x, y):
    screen.blit(playerimg, (playerX, playerY))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (enemyX[i], enemyY[i]))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 2, y - 30))


def isCollision(x, y, x1, y1):
    distance = math.sqrt((math.pow(x - x1, 2)) + (math.pow(y - y1, 2)))
    if distance <= 30:
        return True


# Game Loop

running = True
while running:

    screen.fill((0, 0, 0))
    background = pygame.transform.scale(background, (800, 600))

    screen.blit(background, ((0, 0)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -5
            if event.key == pygame.K_RIGHT:
                player_change = +5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0
    playerX += player_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyx_change[i]
        if enemyX[i] <= 0:
            enemyY[i] += enemyy_change[i]
            enemyx_change[i] = 7
        elif enemyX[i] >= 730:
            enemyY[i] += enemyy_change[i]
            enemyx_change[i] = -7
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_explosion = mixer.Sound('explosion.wav')
            bullet_explosion.play()
            enemyX[i] = random.randint(0, 720)
            enemyY[i] = random.randint(50, 150)
            bullet_state = "ready"
            bulletY = 400
            score_value += 1
            print(score_value)
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bullety_change
    player(playerX, playerY)
    score(testX, textY)

    pygame.display.update()
