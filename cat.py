import pygame
import sys


pygame.init()
clock = pygame.time.Clock()


class newCat():
    def __init__(self,type,sprite,attack_sprites, FHEIGHT, FWIDTH, frames):
        self.sprite = sprite
        self.FHEIGHT = FHEIGHT
        self.FWIDTH = FWIDTH
        self.single_frame_width = FWIDTH // frames
        self.frames = frames
        self.frames_list = []
        self.attack_sprites = attack_sprites
        self.attack_list = []
        self.current_frame_index= 0
        self.x = 850
        self.type = type
        self.set_health()
        self.attack = False
        self.start_time = pygame.time.get_ticks()
        self.last_hit_time = 0  # Tracks when the duck was last damaged
        
        self.cooldown_period = 1500  # 1000 milliseconds = 1 second of invincibility

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
        if self.x > 150:
            self.x -=walkspeed
            active_frame = self.frames_list[self.current_frame_index]
            screen.blit(active_frame, (self.x,y))
            self.attack = False
        else:
            active_frame = self.attack_list[self.current_frame_index]
            self.attack = True
            screen.blit(active_frame, (self.x, y))

    def animspeed(self):
        self.current_frame_index = (self.current_frame_index+1) % self.frames

    def set_health(self):
        if self.type == "normal":
            self.health = 90
        elif self.type == "tank":
            self.health = 200
        
    def remove_enemyBase(self,BaseHealth):
        current_time = pygame.time.get_ticks()
        if self.type == "normal" and (current_time - self.last_hit_time > self.cooldown_period):
            self.last_hit_time = current_time  # Reset the cooldown timer
            BaseHealth -=30
        elif self.type == "tank" and (current_time - self.last_hit_time > self.cooldown_period):
            self.last_hit_time = current_time  # Reset the cooldown timer
            BaseHealth -=15
        return BaseHealth
            
