import pygame
import sys

from cat import newCat

#initialize pygame
pygame.init()

#Set the size of the screen
SCREEN_WIDTH = 1200
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
spawnCat = False

attack = False
catColumn = []


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



    screen.fill((255,255,0))
    if spawnCat == True:
        for cat in catColumn:
            if cat.type == "tank":
                cat.activeFrames(walk_speed,screen, 110)
            elif cat.type == "normal":
                cat.activeFrames(walk_speed,screen,150)
    pygame.display.flip()


pygame.quit()
sys.exit()
