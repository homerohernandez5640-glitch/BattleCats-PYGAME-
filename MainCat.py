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


frames = []
NormalFramenum = 7
normalCat = newCat(NormalCatWalk,frames, NormalCatWalk.get_height(), NormalCatWalk.get_width(), NormalFramenum)


normalCat.animateCat()


current_frame_index = 0
animation_timer = 0
ANIMATION_SPEED = 100

running = True
while running:

    dt = clock.tick(60)  
    animation_timer += dt


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




    if animation_timer >= ANIMATION_SPEED:
        animation_timer = 0
        current_frame_index = (current_frame_index+1) % NormalFramenum
    



    screen.fill((255,255,0))
    active_frame = frames[current_frame_index]
    screen.blit(active_frame, (150,100))
    pygame.display.flip()


pygame.quit()
sys.exit()
