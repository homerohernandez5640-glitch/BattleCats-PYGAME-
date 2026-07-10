import pygame
import sys


pygame.init()

class newCat():
    def __init__(self,sprite,attack_sprites, FHEIGHT, FWIDTH, frames):
        self.sprite = sprite
        self.FHEIGHT = FHEIGHT
        self.FWIDTH = FWIDTH
        self.single_frame_width = FWIDTH // frames
        self.frames = frames
        self.frames_list = []
        self.attack_sprites = attack_sprites
        self.attack_list = []
        self.current_frame_index= 0
        self.x = 1000
    def animateCat(self):
        for i in range(self.frames):
            x_position = i*self.single_frame_width
            y_position = 0
            

            frame_rect = pygame.Rect(x_position, y_position, self.single_frame_width, self.FHEIGHT)
            frame_surface = self.sprite.subsurface(frame_rect)
            frame_surfaceA = self.attack_sprites.subsurface(frame_rect)
            self.frames_list.append(frame_surface)
            self.attack_list.append(frame_surfaceA)
    def activeFrames(self,walkspeed,screen, y):
        if self.x > 200:
            self.x -=walkspeed
            active_frame = self.frames_list[self.current_frame_index]
            screen.blit(active_frame, (self.x,y))
        else:
            active_frame = self.attack_list[self.current_frame_index]
            screen.blit(active_frame, (self.x, y))
    def animspeed(self):
        self.current_frame_index = (self.current_frame_index+1) % self.frames
        
        
