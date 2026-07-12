import pygame
import sys
import random

from cat import newCat
from cat import newEnemy
from cat import GhostFX
from cat import WalletManage

# Initialize pygame
pygame.init()

# Set the size of the screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800

# Display the screen with the size we just set
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set title for game
pygame.display.set_caption("BATTLE CATS")

# This is the game's timer that is counted with ticks
clock = pygame.time.Clock()

# Load and scale environment assets
backgroundImage = pygame.image.load("backgrounds/1background.png")
backgroundImage = pygame.transform.scale(backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

catBaseImage = pygame.image.load("battleCatsAnimations/catbase.png")
catBaseImage = pygame.transform.scale(catBaseImage, (150, 300))

enemyBase = pygame.image.load("battleCatsAnimations/enemybase.png").convert_alpha()

# Set up UI fonts
HealthText = pygame.font.SysFont(None, 40)
Wallet = pygame.font.SysFont(None,40)
upgrade = pygame.font.SysFont(None,40)
upgradewallettext = pygame.font.SysFont(None,25)
NormalPriceText = pygame.font.SysFont(None,25)
TankPriceText = pygame.font.SysFont(None,25)
AxePriceText = pygame.font.SysFont(None,25)

# Load Sprite Sheets
NormalCatWalk = pygame.image.load("battleCatsAnimations/normalcatwalk.png").convert_alpha()
TankCatWalk = pygame.image.load("battleCatsAnimations/tankwalk.png").convert_alpha()
AxeWalk = pygame.image.load("battleCatsAnimations/axewalk.png").convert_alpha()
NormalAttack = pygame.image.load("battleCatsAnimations/normalattack.png").convert_alpha()
TankAttack = pygame.image.load("battleCatsAnimations/tankattack.png").convert_alpha()
AxeAttack = pygame.image.load("battleCatsAnimations/axeattack.png").convert_alpha()

SnakeWalk = pygame.image.load("battleCatsAnimations/snakewalk.png").convert_alpha()
SnakeAttack = pygame.image.load("battleCatsAnimations/snakeattack.png").convert_alpha()
dogwalk = pygame.image.load("battleCatsAnimations/dogwalk.png").convert_alpha()
dogattack = pygame.image.load("battleCatsAnimations/dogattack.png").convert_alpha()

ghost_img = pygame.image.load("battleCatsAnimations/ghost.png").convert_alpha()

# Game State Data Lists and Variables
catColumn = []
enemyColumn = []

ghostColumn = []


CatBaseHealth = 1000
TotalCatBase = CatBaseHealth
EnemyBaseHealth = 1000
TotalEnemyBase = EnemyBaseHealth
NormalFramenum = 7
CurrentWallet = 0
TotalWallet = 2000
Walletmultiplier = 1
upgradePrice = 500
animation_timer = 0
ANIMATION_SPEED = 200
walk_speed = 2

cat_icon_rect = pygame.Rect(0, 0, NormalCatWalk.get_width() // NormalFramenum, NormalCatWalk.get_height())
cat_button_icon = NormalCatWalk.subsurface(cat_icon_rect)
cat_button_icon = pygame.transform.scale(cat_button_icon,(75,75))

tank_icon_rect = pygame.Rect(0, 0, TankCatWalk.get_width() // NormalFramenum, TankCatWalk.get_height())
tank_button_icon = TankCatWalk.subsurface(tank_icon_rect)
tank_button_icon = pygame.transform.scale(tank_button_icon,(50,60))

axe_icon_rect = pygame.Rect(0, 0, AxeWalk.get_width() // NormalFramenum, AxeWalk.get_height())
axe_button_icon = AxeWalk.subsurface(axe_icon_rect)
axe_button_icon = pygame.transform.scale(axe_button_icon,(50,60))


money = WalletManage(CurrentWallet,TotalWallet, Walletmultiplier,upgradePrice)
running = True
while running:

    # Limit frame rate to 30 FPS and track elapsed time
    dt = clock.tick(30)
    animation_timer += dt

    # --- 1. HANDLE PLAYER INPUT AND USER EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and CurrentWallet >= 50 and newCat.can_spawn("normal"):
                newCat.update_spawn_time("normal")
                money.currentWallet -=50  
                normalCat = newCat("normal", NormalCatWalk, NormalAttack, NormalCatWalk.get_height(), NormalCatWalk.get_width(), NormalFramenum)
                normalCat.animateCat()  # Slices frames once upon initialization
                catColumn.append(normalCat)
            elif event.key == pygame.K_2 and CurrentWallet >= 150 and newCat.can_spawn("tank"):
                newCat.update_spawn_time("tank")
                money.currentWallet -=150
                tankCat = newCat("tank", TankCatWalk, TankAttack, TankCatWalk.get_height(), TankCatWalk.get_width(), NormalFramenum)
                tankCat.animateCat()    # Slices frames once upon initialization
                catColumn.append(tankCat)
            elif event.key == pygame.K_u and money.upgradePrice <= money.currentWallet:
                money.upgrade()
                Walletmultiplier = money.GainMultiplier
                CurrentWallet = money.currentWallet
                TotalWallet = money.TotalWallet
                upgradePrice = upgradePrice
            elif event.key == pygame.K_3 and CurrentWallet >= 350 and newCat.can_spawn("axe"):
                newCat.update_spawn_time("axe")
                money.currentWallet -=350
                AxeCat = newCat("axe", AxeWalk, AxeAttack, AxeWalk.get_height(), AxeWalk.get_width(), NormalFramenum)
                AxeCat.animateCat()  # Slices frames once upon initialization
                catColumn.append(AxeCat)
                
    # --- 2. AUTOMATED ENEMY SPRAWNING ---
    randSpawn = random.randint(1, 6000)                                                                            
    if randSpawn <= 10:
        Dog = newEnemy("dog", dogwalk, dogattack, dogwalk.get_height(), dogwalk.get_width(), NormalFramenum)
        Dog.animateEnemy() # Slices frames once upon initialization
        enemyColumn.append(Dog)
    elif randSpawn >=10 and randSpawn <=15:
        Snake = newEnemy("snake", SnakeWalk, SnakeAttack, SnakeWalk.get_height(), SnakeWalk.get_width(), NormalFramenum)
        Snake.animateEnemy()
        enemyColumn.append(Snake)


    # --- 3. FILTER OUT DEAD CHARACTER OBJECTS AND SPAWN GHOSTS ---
    for cat in catColumn:
        if cat.health <= 0:
            # Spawn a ghost at the center of the dying cat
            ghostColumn.append(GhostFX(cat.x + 20, 560, ghost_img))
    catColumn = [cat for cat in catColumn if cat.health > 0]

    for enemy in enemyColumn:
        if enemy.health <= 0:
            # Spawn a ghost at the center of the dying enemy
            if enemy.type == "dog":
                money.currentWallet += 75
            elif enemy.type == "snake":
                money.currentWallet +=100
            ghostColumn.append(GhostFX(enemy.x + 20, 560, ghost_img))
    enemyColumn = [enemy for enemy in enemyColumn if enemy.health > 0]


    # --- 4. STEP SPRITE FRAME ANIMATIONS ---
    if animation_timer >= ANIMATION_SPEED:
        animation_timer = 0
        for cat in catColumn:
            cat.animspeed()
        for enemy in enemyColumn:
            enemy.animspeed()

    # --- 5. DISTANCE CHECKS & SINGLE-TARGET LOCKING ---
    # Cats search for an enemy target directly ahead of them
    for cat in catColumn:
        if cat.target and cat.target.health <= 0:
            cat.target = None
            
        if cat.target is None and cat.x > 40:
            for enemy in enemyColumn:
                # If an opposing unit is close enough, engage target lock
                if enemy.x < cat.x and (cat.x - enemy.x) <= 60:
                    cat.target = enemy
                    break  # Break ensures it targets only a single enemy unit

    # Enemies search for a cat target directly ahead of them
    for enemy in enemyColumn:
        if enemy.target and enemy.target.health <= 0:
            enemy.target = None
            
        if enemy.target is None and enemy.x < 820:
            for cat in catColumn:
                # If a friendly unit is close enough, engage target lock
                if cat.x > enemy.x and (cat.x - enemy.x) <= 60:
                    enemy.target = cat
                    break  # Break ensures it targets only a single cat unit

    # --- 6. DAMAGE INTERACTION PROCESSING ---
    current_time = pygame.time.get_ticks()

    for cat in catColumn:
        if cat.attack:
            if cat.target is not None:
                # Deal damage directly to the single target it is locked on to
                if current_time - cat.last_hit_time > cat.cooldown_period:
                    cat.last_hit_time = current_time
                    if cat.type == "normal":
                        cat.target.health -= 30
                    elif cat.type == "tank":
                        cat.target.health -=15
                    elif cat.type == "axe":
                        cat.target.health -=50
                    else:
                        cat.target.health -=15
                
            elif cat.x <= 130:
                # Attack the main enemy base only if no unit is blocking the way
                EnemyBaseHealth = cat.remove_enemyBase(EnemyBaseHealth)

    for enemy in enemyColumn:
        if enemy.attack:
            if enemy.target is not None:
                # Deal damage directly to the single target it is locked on to
                if current_time - enemy.last_hit_time > enemy.cooldown_period:
                    enemy.last_hit_time = current_time
                    if enemy.type == "dog":
                        enemy.target.health -= 30
                    elif enemy.type == "snake":
                        enemy.target.health -= 45
                    else:
                        enemy.target.health -= 15
            elif enemy.x >= 790:
                # Attack the main friendly base only if no unit is blocking the way
                CatBaseHealth = enemy.remove_catBase(CatBaseHealth)
    #increment wallet
    CurrentWallet = money.increment()
    # --- 7. RENDERING SCENE GRAPHICS ---
    # Draw environmental layout
    screen.fill((255, 255, 0))
    screen.blit(backgroundImage, (0, 0))
    screen.blit(catBaseImage, (850, 360))
    screen.blit(enemyBase, (40, 395))

    # Convert UI integers into readable typography graphics
    CatBaseHealthR = HealthText.render(str(CatBaseHealth)+"/"+str(TotalCatBase), True, (0, 0, 0))
    EnemyBaseHealthR = HealthText.render(str(EnemyBaseHealth)+"/"+str(TotalEnemyBase), True, (0, 0, 0))
    WalletText = Wallet.render(str(CurrentWallet)+"/"+str(TotalWallet), True,(0 ,0 , 0))
    upgrades = upgrade.render("UPGRADE", True, (255,255,0))
    upgradewallettexts = upgradewallettext.render(str(money.upgradePrice),True,(255,255,0))
    screen.blit(CatBaseHealthR, (850, 330))
    screen.blit(EnemyBaseHealthR, (40, 350))
    screen.blit(WalletText,(870,40))
    

   

    if money.currentWallet >= money.upgradePrice:
        pygame.draw.rect(screen, (255, 120, 0), (20, 690, 200, 50))
    else:
        pygame.draw.rect(screen, (100, 255, 0), (20, 690, 200, 50))
    screen.blit(upgrades, (40,700))
    screen.blit(upgradewallettexts, (100,725))

    if money.currentWallet >= 50 and newCat.can_spawn("normal"):
        pygame.draw.rect(screen, (255, 255, 255), (400, 690, 100, 50))
    else:
        pygame.draw.rect(screen, (120, 120, 120), (400, 690, 100, 50))
    
    if money.currentWallet >= 150 and newCat.can_spawn("tank"):
        pygame.draw.rect(screen, (255, 255, 255), (550, 690, 100, 50))
    else:
        pygame.draw.rect(screen, (120, 120, 120), (550, 690, 100, 50))

    if money.currentWallet >= 350 and newCat.can_spawn("axe"):
        pygame.draw.rect(screen, (255, 255, 255), (700, 690, 100, 50))
    else:
        pygame.draw.rect(screen, (120, 120, 120), (700, 690, 100, 50))

    screen.blit(tank_button_icon,(575,680))
    screen.blit(cat_button_icon,(410,665))
    screen.blit(axe_button_icon,(725,680))
    screen.blit(upgrades, (40,700))
    screen.blit(upgradewallettexts, (100,725))
    NormalPrice = NormalPriceText.render("50", True,(0 ,0 , 0))
    TankPrice = TankPriceText.render("150", True,(0 ,0 , 0))
    AxePrice = AxePriceText.render("350", True,(0 ,0 , 0))
    screen.blit(NormalPrice,(400,690))
    screen.blit(TankPrice,(550,690))
    screen.blit(AxePrice,(700,690)) 

    # Draw active ally units onto the view screen matrix
    for cat in catColumn:
        if cat.type == "tank":
            cat.activeFrames(walk_speed, screen, 520)
        elif cat.type == "normal":
            cat.activeFrames(walk_speed, screen, 560)
        elif cat.type == "axe":
            cat.activeFrames(walk_speed, screen, 560)

    # Draw active enemy units onto the view screen matrix
    for enemy in enemyColumn:
        enemy.activeFrames(walk_speed, screen, 580)


    # --- DRAW FLOATING GHOST EFFECTS ---
    # Update position, drop alpha, and render
    for ghost in ghostColumn:
        ghost.update_and_draw(screen)
        
    # Garbage collection: remove ghosts that have completely faded out
    ghostColumn = [ghost for ghost in ghostColumn if ghost.alpha > 0]


    # Flip front and back draw buffers to update visual interface
    pygame.display.flip()

# Safe application lifecycle cleanup when loop terminates
pygame.quit()
sys.exit()

