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


# Load Sprite Sheets
NormalCatWalk = pygame.image.load("battleCatsAnimations/normalcatwalk.png").convert_alpha()
TankCatWalk = pygame.image.load("battleCatsAnimations/tankwalk.png").convert_alpha()
NormalAttack = pygame.image.load("battleCatsAnimations/normalattack.png").convert_alpha()
TankAttack = pygame.image.load("battleCatsAnimations/tankattack.png").convert_alpha()

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
            if event.key == pygame.K_1 and CurrentWallet >= 50:
                money.currentWallet -=50  
                normalCat = newCat("normal", NormalCatWalk, NormalAttack, NormalCatWalk.get_height(), NormalCatWalk.get_width(), NormalFramenum)
                normalCat.animateCat()  # Slices frames once upon initialization
                catColumn.append(normalCat)
            elif event.key == pygame.K_2 and CurrentWallet >= 150:
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

                
    # --- 2. AUTOMATED ENEMY SPRAWNING ---
    randSpawn = random.randint(1, 2000)                                                                            
    if randSpawn <= 5:
        Dog = newEnemy("dog", dogwalk, dogattack, dogwalk.get_height(), dogwalk.get_width(), NormalFramenum)
        Dog.animateEnemy() # Slices frames once upon initialization
        enemyColumn.append(Dog)


    # --- 3. FILTER OUT DEAD CHARACTER OBJECTS AND SPAWN GHOSTS ---
    for cat in catColumn:
        if cat.health <= 0:
            # Spawn a ghost at the center of the dying cat
            ghostColumn.append(GhostFX(cat.x + 20, 560, ghost_img))
    catColumn = [cat for cat in catColumn if cat.health > 0]

    for enemy in enemyColumn:
        if enemy.health <= 0:
            # Spawn a ghost at the center of the dying enemy
            money.currentWallet += 75
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
                    cat.target.health -= 30 if cat.type == "normal" else 15
            elif cat.x <= 130:
                # Attack the main enemy base only if no unit is blocking the way
                EnemyBaseHealth = cat.remove_enemyBase(EnemyBaseHealth)

    for enemy in enemyColumn:
        if enemy.attack:
            if enemy.target is not None:
                # Deal damage directly to the single target it is locked on to
                if current_time - enemy.last_hit_time > enemy.cooldown_period:
                    enemy.last_hit_time = current_time
                    enemy.target.health -= 30 if enemy.type == "dog" else 15
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
    screen.blit(CatBaseHealthR, (850, 330))
    screen.blit(EnemyBaseHealthR, (40, 350))
    screen.blit(WalletText,(870,40))

    if money.currentWallet >= money.upgradePrice:
        pygame.draw.rect(screen, (255, 120, 0), (20, 690, 200, 50))
    else:
        pygame.draw.rect(screen, (100, 255, 0), (20, 690, 200, 50))
    screen.blit(upgrades, (40,700))

    # Draw active ally units onto the view screen matrix
    for cat in catColumn:
        if cat.type == "tank":
            cat.activeFrames(walk_speed, screen, 520)
        elif cat.type == "normal":
            cat.activeFrames(walk_speed, screen, 560)

    # Draw active enemy units onto the view screen matrix
    for enemy in enemyColumn:
        enemy.activeFrames(walk_speed, screen, 560)


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
