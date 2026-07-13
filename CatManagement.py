import pygame
from cat import newCat
from cat import newEnemy
from cat import GhostFX
from cat import WalletManage




class newCatMan():
    def __init__(self,price,type,walk, attack, framenum, target_list,money, range):
        self.price = price
        self.type = type
        self.framenum = framenum
        self.wallet = money
        self.attack = attack
        self.walk = walk
        self.list = target_list
        self.range = range

    def try_spawn_cat(self):
        if self.wallet.currentWallet >= self.price and newCat.can_spawn(self.type):
           newCat.update_spawn_time(self.type)
           self.wallet.currentWallet -= self.price
           spawned_unit = newCat(self.type, self.walk, self.attack, self.walk.get_height(), self.walk.get_width(), self.framenum, self.range)
           spawned_unit.animateCat()
           self.list.append(spawned_unit)

class catBox():
    def __init__(self,money,price, catColumn, type, x, screen, walk, iconX , iconY,text, framenum, iconheight, iconwidth):
        self.wallet = money
        self.price = price
        self.list = catColumn
        self.type = type
        self.screen = screen
        self.framenum = framenum
        self.x = x
        self.walk = walk
        self.iconX = iconX
        self.iconY = iconY
        self.text = text
        self.iconheight = iconheight
        self.iconwidth = iconwidth

    def printCatBox(self):
        cat_icon_rect = pygame.Rect(0, 0, self.walk.get_width() // self.framenum, self.walk.get_height())
        cat_button_icon = self.walk.subsurface(cat_icon_rect)
        cat_button_icon = pygame.transform.scale(cat_button_icon,(self.iconheight,self.iconwidth))
        
        if self.wallet.currentWallet >= self.price and newCat.can_spawn(self.type):
            pygame.draw.rect(self.screen, (255,255,255),(self.x,690,100,50))
        else:
            pygame.draw.rect(self.screen, (120,120,120),(self.x,690,100,50))
        self.screen.blit(cat_button_icon,(self.iconX,self.iconY))
        icons = self.text.render(str(self.price), True, (0,0,0))
        self.screen.blit(icons,(self.x,690))
