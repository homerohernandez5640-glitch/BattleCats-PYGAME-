import pygame
import sys

from cat import newCat

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


spawnCat = False

attack = False
catColumn = []

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
                spawnCat = True
                for cat in catColumn:
                    cat.animateCat()
            elif event.key == pygame.K_2:
                tankCat = newCat("tank",TankCatWalk, TankAttack, TankCatWalk.get_height(),TankCatWalk.get_width(), 7)
                catColumn.append(tankCat)
                spawnCat = True
                for cat in catColumn:
                    cat.animateCat()

    if spawnCat == True:
        if animation_timer >= ANIMATION_SPEED:
            animation_timer = 0
            for cat in catColumn:
                cat.animspeed()


        for cat in catColumn:
            if cat.attack == True:
                EnemyBaseHealth = cat.remove_enemyBase(EnemyBaseHealth)




    screen.fill((255,255,0))
    screen.blit(backgroundImage,(0,0))
    screen.blit(catBaseImage, (850,360))
    screen.blit(enemyBase,(40,395))

    CatBaseHealthR = HealthText.render(str(CatBaseHealth), True, (0, 0, 0))
    EnemyBaseHealthR = HealthText.render(str(EnemyBaseHealth), True, (0, 0, 0))

    screen.blit(CatBaseHealthR, (850,330))
    screen.blit(EnemyBaseHealthR, (40, 350))

    if spawnCat == True:
        for cat in catColumn:
            if cat.type == "tank":
                cat.activeFrames(walk_speed,screen, 510)
            elif cat.type == "normal":
                cat.activeFrames(walk_speed,screen,550)
    pygame.display.flip()


pygame.quit()
sys.exit()
