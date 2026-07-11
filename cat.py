import pygame

class newCat():

    last_normal_spawn_time = 0
    last_tank_spawn_time = 0
    
    NORMAL_COOLDOWN = 3000  # 3 seconds
    TANK_COOLDOWN = 5000    # 5 seconds

    def __init__(self, cat_type, sprite, attack_sprites, FHEIGHT, FWIDTH, frames):
        self.sprite = sprite
        self.FHEIGHT = FHEIGHT
        self.FWIDTH = FWIDTH
        self.single_frame_width = FWIDTH // frames
        self.frames = frames
        self.frames_list = []
        self.attack_sprites = attack_sprites
        self.attack_list = []
        self.current_frame_index = 0
        self.x = 850
        self.type = cat_type
        self.set_health()
        self.attack = False
        self.start_time = pygame.time.get_ticks()
        self.last_hit_time = 0  
        self.cooldown_period = 1500  
        self.target = None  # Tracks the specific enemy this cat is fighting




    # A class method lets you check if a cat can spawn without needing an alive cat object
    @classmethod
    def can_spawn(cls, cat_type):
        current_time = pygame.time.get_ticks()
        if cat_type == "normal":
            return (current_time - cls.last_normal_spawn_time) >= cls.NORMAL_COOLDOWN
        elif cat_type == "tank":
            return (current_time - cls.last_tank_spawn_time) >= cls.TANK_COOLDOWN
        return False


    # A class method to update the shared timestamp when a cat is successfully deployed
    @classmethod
    def update_spawn_time(cls, cat_type):
        current_time = pygame.time.get_ticks()
        if cat_type == "normal":
            cls.last_normal_spawn_time = current_time
        elif cat_type == "tank":
            cls.last_tank_spawn_time = current_time


    def animateCat(self):
        self.frames_list.clear()
        self.attack_list.clear()
        for i in range(self.frames):
            x_position = i * self.single_frame_width
            y_position = 0
            frame_rect = pygame.Rect(x_position, y_position, self.single_frame_width, self.FHEIGHT)
            frame_surface = self.sprite.subsurface(frame_rect)
            frame_surfaceA = self.attack_sprites.subsurface(frame_rect)
            self.frames_list.append(frame_surface)
            self.attack_list.append(frame_surfaceA)

    def activeFrames(self, walkspeed, screen, y):
        # Stop walking and switch to attack animation if fighting a target or at base
        if self.target is not None or self.x <= 130:
            active_frame = self.attack_list[self.current_frame_index]
            self.attack = True
            screen.blit(active_frame, (self.x, y))
        else:
            self.x -= walkspeed
            active_frame = self.frames_list[self.current_frame_index]
            screen.blit(active_frame, (self.x, y))
            self.attack = False

    def animspeed(self):
        if self.frames > 0:
            self.current_frame_index = (self.current_frame_index + 1) % self.frames

    def set_health(self):
        if self.type == "normal":
            self.health = 90
        elif self.type == "tank":
            self.health = 200

    def remove_enemyBase(self, BaseHealth):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.cooldown_period:
            self.last_hit_time = current_time  
            if self.type == "normal":
                BaseHealth -= 30
            elif self.type == "tank":
                BaseHealth -= 15
        return BaseHealth                                                                                                      

class newEnemy():
    def __init__(self, enemy_type, sprite, attack_sprites, FHEIGHT, FWIDTH, frames):
        self.sprite = sprite
        self.FHEIGHT = FHEIGHT
        self.FWIDTH = FWIDTH
        self.single_frame_width = FWIDTH // frames
        self.frames = frames
        self.frames_list = []
        self.attack_sprites = attack_sprites
        self.attack_list = []
        self.current_frame_index = 0
        self.x = 40
        self.type = enemy_type
        self.set_health()
        self.attack = False
        self.start_time = pygame.time.get_ticks()
        self.last_hit_time = 0  
        self.cooldown_period = 1500  
        self.target = None  # FIX: Added missing single-target tracking attribute

    def animateEnemy(self):
        self.frames_list.clear()
        self.attack_list.clear()
        for i in range(self.frames):
            x_position = i * self.single_frame_width
            y_position = 0
            frame_rect = pygame.Rect(x_position, y_position, self.single_frame_width, self.FHEIGHT)
            frame_surface = self.sprite.subsurface(frame_rect)
            frame_surfaceA = self.attack_sprites.subsurface(frame_rect)
            self.frames_list.append(frame_surface)
            self.attack_list.append(frame_surfaceA)

    def activeFrames(self, walkspeed, screen, y):
        # Stop walking and switch to attack animation if fighting a target or at base
        if self.target is not None or self.x >= 790:
            active_frame = self.attack_list[self.current_frame_index]
            self.attack = True
            screen.blit(active_frame, (self.x, y))
        else:
            if self.type == "dog":
                self.x += walkspeed
            elif self.type == "snake":
                self.x += (walkspeed + 1)
            active_frame = self.frames_list[self.current_frame_index]
            screen.blit(active_frame, (self.x, y))
            self.attack = False

    def animspeed(self):
        if self.frames > 0:
            self.current_frame_index = (self.current_frame_index + 1) % self.frames

    def set_health(self):
        if self.type == "dog":
            self.health = 90
        elif self.type == "snake":
            self.health = 120

    def remove_catBase(self, BaseHealth):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.cooldown_period:
            self.last_hit_time = current_time  
            if self.type == "dog":
                BaseHealth -= 30
            elif self.type == "snake":
                BaseHealth -= 15
        return BaseHealth



class GhostFX():
    def __init__(self, start_x, start_y, ghost_image):
        # Scale the ghost image down slightly so it fits nicely over characters
        self.image = pygame.transform.scale(ghost_image, (40, 40))
        self.x = start_x
        self.y = start_y
        self.alpha = 255  # Opacity tracker for a clean fade-out effect

    def update_and_draw(self, screen, rise_speed=3):
        # Move straight up
        self.y -= rise_speed
        # Slowly fade out over time
        self.alpha -= 5
        
        if self.alpha > 0:
            # Set image transparency surface data dynamically
            self.image.set_alpha(self.alpha)
            screen.blit(self.image, (self.x, self.y))

class WalletManage():
    def __init__(self,currentWallet,TotalWallet,GainMultiplier, upgradePrice):
        self.currentWallet = currentWallet
        self.TotalWallet = TotalWallet
        self.GainMultiplier = GainMultiplier
        self.upgradePrice = upgradePrice
        self.start_time = pygame.time.get_ticks()
        self.cooldown_period = 150
        self.last_hit_time = 0
        self.increments = 1

    def increment(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.cooldown_period and self.currentWallet < self.TotalWallet:
            self.last_hit_time = current_time
            self.currentWallet += self.increments*self.GainMultiplier 
        return self.currentWallet
    def upgrade(self):
        self.GainMultiplier +=1
        self.TotalWallet +=self.TotalWallet
        self.currentWallet -=self.upgradePrice
        self.upgradePrice +=self.upgradePrice
        self.cooldown_period -=25
