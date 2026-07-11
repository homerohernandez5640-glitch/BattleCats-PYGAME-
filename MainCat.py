import pygame
import sys
import random

from cat import newCat
from cat import newEnemy
#initialize pygame
pygame.init()

#Set the size of the screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800

#display the screen with the size we just set
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#set title for game
pygame.display.set_caption("BATTLE CATS")

#This is the game's timer that is counted with ticks
clock = pygame.time.Clock()

#I set the sprite sheet, but we have to slice this to actually fit here
NormalCatWalk = pygame.image.load("battleCatsAnimations/normalcatwalk.png").convert_alpha()
TankCatWalk = pygame.image.load("battleCatsAnimations/tankwalk.png").convert_alpha()
NormalAttack = pygame.image.load("battleCatsAnimations/normalattack.png").convert_alpha()
TankAttack = pygame.image.load("battleCatsAnimations/tankattack.png").convert_alpha()
catBaseImage = pygame.image.load("battleCatsAnimations/catbase.png")
backgroundImage = pygame.image.load("backgrounds/1background.png")
backgroundImage = pygame.transform.scale(backgroundImage,(SCREEN_WIDTH, SCREEN_HEIGHT))
catBaseImage = pygame.transform.scale(catBaseImage,(150,300))
HealthText = pygame.font.SysFont(None,40)
enemyBase = pygame.image.load("battleCatsAnimations/enemybase.png").convert_alpha()


dogwalk = pygame.image.load("battleCatsAnimations/dogwalk.png").convert_alpha()
dogattack = pygame.image.load("battleCatsAnimations/dogattack.png").convert_alpha()

spawnCat = False
spawnEnemy = False
attack = False
catColumn = []
enemyColumn = []

CatBaseHealth = 1000
EnemyBaseHealth = 1000
NormalFramenum = 7


animation_timer = 0
ANIMATION_SPEED = 200
walk_speed = 2
cat_x = SCREEN_WIDTH

running = True
while running:

    dt = clock.tick(30)  
    animation_timer += dt



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                normalCat = newCat("normal",NormalCatWalk,NormalAttack, NormalCatWalk.get_height(), NormalCatWalk.get_width(), NormalFramenum)
                catColumn.append(normalCat)
                normalCat.animateCat()
                spawnCat = True
                
            elif event.key == pygame.K_2:
                tankCat = newCat("tank",TankCatWalk, TankAttack, TankCatWalk.get_height(),TankCatWalk.get_width(), NormalFramenum)
                catColumn.append(tankCat)
                tankCat.animateCat()
                spawnCat = True

    randSpawn = random.randint(1,2000)
    
    if randSpawn <= 30:
        Dog = newEnemy("dog",dogwalk,dogattack,dogwalk.get_height(), dogwalk.get_width(), NormalFramenum) 
        enemyColumn.append(Dog)
        Dog.animateEnemy()
        spawnEnemy = True
        
    if animation_timer >= ANIMATION_SPEED:
        animation_timer = 0
        for cat in catColumn:
            cat.animspeed()
        for enemy in enemyColumn:
            enemy.animspeed()

    for cat in catColumn:
        if cat.attack == True:
            EnemyBaseHealth = cat.remove_enemyBase(EnemyBaseHealth)

    for enemy in enemyColumn:
        if enemy.attack == True:
            CatBaseHealth = enemy.remove_catBase(CatBaseHealth)


    screen.fill((255,255,0))
    screen.blit(backgroundImage,(0,0))
    screen.blit(catBaseImage, (850,360))
    screen.blit(enemyBase,(40,395))

    CatBaseHealthR = HealthText.render(str(CatBaseHealth), True, (0, 0, 0))
    EnemyBaseHealthR = HealthText.render(str(EnemyBaseHealth), True, (0, 0, 0))

    screen.blit(CatBaseHealthR, (850,330))
    screen.blit(EnemyBaseHealthR, (40, 350))

    for cat in catColumn:
        if cat.type == "tank":
            cat.activeFrames(walk_speed,screen, 520)
        elif cat.type == "normal":
            cat.activeFrames(walk_speed,screen,560)

    for enemy in enemyColumn:
        enemy.activeFrames(walk_speed,screen,560)

    pygame.display.flip()


pygame.quit()
sys.exit()
