import pygame
from pygame import mixer
import random
import math

#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

# background image

background = pygame.image.load("background.jpg")

#img for game over
game_over_img = pygame.image.load("game-over.png")

#text for game over
over_text = pygame.font.Font("italic.ttf",64)
#making screen show game over
gameX = 370
gameY = 120

def game_over_text():
    overing_text = over_text.render("GAME OVER",True,(0,0,0))
    screen.blit(overing_text,(250,250))

def game_over_image(x,y):
    screen.blit(game_over_img,(x,y))



#background sound
mixer.music.load("sound_game.MP3")
mixer.music.play(-1)

#make title of this game
pygame.display.set_caption('testing')

# make icon for this game
icon = pygame.image.load("ship_space.png")
pygame.display.set_icon(icon)

#making player image
playerimg = pygame.image.load("player.png")

playerX = 370
playerY = 480
playerX_change = 0

#making action for player
def player(x,y):
    screen.blit(playerimg,(x,y))

#making enemy image
enemy_number = 60
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(enemy_number):
        
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,764))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(60)

#making enemy moving
def enemy(x, y,i):
    screen.blit(enemyimg[i],(x,y))

#making bullet image 
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
#ready mean bullet cant moving
bullet_state = "ready"

#making bullet moving
def fire_bullet(x,y):
    global bullet_state
    #fire mean bullet moving
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16,y+10))


#making bullet defeating the enemy

def defeat_enemy(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else: 
        return False
    
#making score show in screen
score = 0
font = pygame.font.Font("italic.ttf",40)
textX = 10
textY = 10
def score_show(x,y):
    scoring = font.render("score :" + str(score),True,(255,255,255))
    screen.blit(scoring,(x,y))


running = True
while running:
    #for background color using rgb color
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #making the player move
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_music = mixer.Sound("laser.wav")
                    bullet_music.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #this for movement of player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 765:
        playerX = 765

    # this for movement of the enemy
    for i in range(enemy_number):
        #game over
        if enemyY[i] > 460:
            for j in range(enemy_number):
                enemyY[j] = 2000
            game_over_image(gameX,gameY)
            game_over_text()
            break

            

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 765:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
    for k in range(enemy_number):
        defeat = defeat_enemy(enemyX[k],enemyY[k],bulletX,bulletY)
        if defeat:
            explosion_music = mixer.Sound("explosion.wav")
            explosion_music.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            # enemyY[i] = 40
            # for k in range(enemy_number):

            enemyX[k] = random.randint(0,764)
            enemyY[k] = -2000 
        enemy(enemyX[k],enemyY[k],k)

    #this for making bullet fire moving
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    #defeat enemy

        
    player(playerX,playerY)
    score_show(textX,textY)
    # apply the background color
    pygame.display.update()
    