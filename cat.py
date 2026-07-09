import pygame
import sys


pygame.init()

class newCat():
    def __init__(self,sprite,frames_list, FHEIGHT, FWIDTH, frames):
        self.sprite = sprite
        self.FHEIGHT = FHEIGHT
        self.FWIDTH = FWIDTH
        self.single_frame_width = FWIDTH // frames
        self.frames = frames
        self.frames_list = frames_list
   
    def animateCat(self):
        for i in range(self.frames):
            x_position = i*self.single_frame_width
            y_position = 0
            

            frame_rect = pygame.Rect(x_position, y_position, self.single_frame_width, self.FHEIGHT)
            frame_surface = self.sprite.subsurface(frame_rect)
            self.frames_list.append(frame_surface)

