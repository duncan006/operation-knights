import sys
import random
import pygame
pygame.init()

fps = 30
WINDOW_HEIGHT = 300
WINDOW_WIDTH = 600

enemyList = []

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pygame.time.Clock()

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255,0,0)
        self.height = 30
        self.width = 30
        self.speed = 10


class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.height = 50
        self.width = 20
        self.speed = 5
        self.jumpCount = 0
        self.jumping = False
        self.jumpMult = 3
        self.jumpList = [6,6,6,6,6,4,4,4,4,2,2,2,1,1,0,-1,-1,-2,-2,-2,-4,-4,-4,-4,-6,-6,-6,-6,-6]
        
        self.heldLeft = False
        self.heldRight = False
        self.crouch = False
        
        
    def special_move_handler(self):
        if self.jumping:
            self.y -= self.jumpMult * self.jumpList[self.jumpCount]
            self.jumpCount += 1
            if self.jumpCount > len(self.jumpList)-1:
                self.jumpCount = 0
                self.jumping = False
                
    def movePlayer(self):
        if self.heldLeft == True:
            self.x -= self.speed
        if self.heldRight == True:
            self.x += self.speed

player = Player(WINDOW_WIDTH/2,WINDOW_HEIGHT-50,(255,0,0))

def dropEnemies(enemyList):
    if random.random() < 0.05:
        if len(enemyList) < 8:
            x_pos = WINDOW_WIDTH
            y_pos = random.randint(0, WINDOW_HEIGHT - 10)
            enemyList.append(Enemy(x_pos, y_pos))

def drawEnemies(enemyList):
    for enemy in enemyList:
        pygame.draw.rect(screen, enemy.color, [enemy.x, enemy.y, enemy.width, enemy.height])

def updateEnemies(enemyList):
    for idx, enemy in enumerate(enemyList):
        enemy.x -= enemy.speed
        if enemy.x < 0:
            enemyList.pop(idx)

def collisionHandler(player, enemyList):
    px = player.x
    py = player.y
    ph = player.height
    pw = player.width
    for enemy in enemyList:
        ex = enemy.x
        ey = enemy.y
        eh = enemy.height
        ew = enemy.width
        if (ex >= px and ex < (px + pw)) or ((px >= ex and px < (ex + ew))):
            if (ey >= py and ey < (py + ph)) or ((py >= ey and py < (ey + eh))):
                running = False
        return False


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_a:
                player.heldLeft = True
            if event.key == pygame.K_d:
                player.heldRight = True
            if event.key == pygame.K_s and player.jumping == False: 
                    change = player.height * 0.4
                    player.y = player.y + player.height - change
                    player.height = change
                    player.crouch = True
                
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                if player.crouch == False:
                    player.jumping = True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.heldLeft = False
            if event.key == pygame.K_d:
                player.heldRight = False
            if event.key == pygame.K_s and player.jumping == False:
                change = player.height / 0.4
                player.y = player.y + player.height - change
                player.height = change
                player.crouch = False
                
        for e in pygame.event.get():
            pass
    
    screen.fill((0,0,0))

    player.special_move_handler()
    player.movePlayer()
    pygame.draw.rect(screen, (0, 0, 255), (int(player.x), int(player.y), int(player.width), int(player.height)))
    
    dropEnemies(enemyList)
    updateEnemies(enemyList)
    drawEnemies(enemyList)
    
    collisionHandler(player, enemyList)
    
    clock.tick(fps)
    
    # Flip the display
    pygame.display.flip()
pygame.quit()
