import pygame
import random
from pygame import mixer
# Initialize the pygame
pygame.init()

# Game Screen
screen = pygame.display.set_mode((800, 600))  # (Width, Height)

# Background
background = pygame.image.load("space.png")

# Background Music
# mixer.music.load("background.wav")
# mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("spaceship.png")
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# Enemy

enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemy_img.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(40)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

game_over_font = pygame.font.Font('freesansbold.ttf', 64)
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    dis = ((bullet_x-enemy_x)**2+(bullet_y-enemy_y)**2)**0.5
    if dis <= 27 and bullet_state == "fire":
        explosion= mixer.Sound("explosion.wav")
        explosion.play()
        return True
    return False

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))

# Game Loop
while True:
    screen.fill((250, 200, 0))
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= 5
            if event.key == pygame.K_RIGHT:
                player_x_change += 5
            if event.key == pygame.K_UP:
                player_y_change -= 5
            if event.key == pygame.K_DOWN:
                player_y_change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            player_x_change = 0
            player_y_change=0
            
    # Restrict Player Movement        
    player_x += player_x_change
    player_y += player_y_change
    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736
    if player_y <= 0:
        player_y = 0
    if player_y >= 536:
        player_y = 536
        
    # Enemy Movement
    for i in range(num_of_enemy):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 3
            enemy_y[i] += enemy_y_change[i]
        if enemy_x[i] >= 736:
            enemy_x_change[i] = -3
            enemy_y[i] += enemy_y_change[i]
        if enemy_y[i] >= 536:
            for j in range(num_of_enemy):
                enemy_y[j]=2000
                game_over()
                break
            
        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
            score_value += 1
        enemy(enemy_x[i], enemy_y[i], i)
        
    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"
        
    player(player_x, player_y)
    show_score(textX, testY)
    pygame.display.update()
