import sys
import random
import pygame
pygame.init()

fps = 30
WINDOW_HEIGHT = 300
WINDOW_WIDTH = 600
spawnRate = 0.06

enemyList = []

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pygame.time.Clock()

scoreFont = pygame.font.SysFont("monospace", 35)

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
        self.crouchHeight = 30
        self.standHeight = 50
        self.height = self.standHeight
        self.width = 20
        self.speed = 5
        self.score = 0
        
        self.jumpCount = 0
        self.jumping = False
        self.jumpMult = 3
        self.jumpList = [6,6,6,6,6,4,4,4,4,2,2,2,1,1,0,-1,-1,-2,-2,-2,-4,-4,-4,-4,-6,-6,-6,-6,-6]
        
        self.heldLeft = False
        self.heldRight = False
        self.crouch = False
        
        
    def special_move_handler(self):
        if self.jumping and not self.crouch:
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

def dropEnemies(enemyList, spawnRate):
    if random.random() < spawnRate:
        if len(enemyList) < 8:
            x_pos = WINDOW_WIDTH
            y_pos = random.randint(0, WINDOW_HEIGHT - 10)
            enemyList.append(Enemy(x_pos, y_pos))

def drawEnemies(enemyList):
    for enemy in enemyList:
        pygame.draw.rect(screen, enemy.color, [enemy.x, enemy.y, enemy.width, enemy.height])

def updateEnemies(enemyList, player):
    for idx, enemy in enumerate(enemyList):
        enemy.x -= enemy.speed
        if enemy.x < 0:
            enemyList.pop(idx)
            player.score += 1

def collisionHandler(player, enemyList):
    keepRunning = True
    for enemy in enemyList:
        if (player.x < enemy.x + enemy.width and player.x + player.width > enemy.x and player.y < enemy.y + enemy.height and player.y + player.height > enemy.y):
            keepRunning = False
    
    if keepRunning:
        return True
    if not keepRunning:
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
            if event.key == pygame.K_s and not player.jumping: 
                player.height = player.crouchHeight
                player.y = player.y + player.standHeight - player.crouchHeight
                player.crouch = True
            if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and not player.crouch:
                player.jumping = True
                
        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_a:
                player.heldLeft = False
            if event.key == pygame.K_d:
                player.heldRight = False
            if event.key == pygame.K_s and not player.jumping and player.crouch:
                player.height = player.standHeight
                player.y = player.y + player.crouchHeight - player.standHeight
                player.crouch = False
                
        for e in pygame.event.get():
            pass
    
    screen.fill((0,0,0))

    player.special_move_handler()
    player.movePlayer()
    pygame.draw.rect(screen, (0, 0, 255), (int(player.x), int(player.y), int(player.width), int(player.height)))
    
    dropEnemies(enemyList, spawnRate)
    updateEnemies(enemyList, player)
    drawEnemies(enemyList)
    
    running = collisionHandler(player, enemyList)
    
    text = "score: " + str(player.score)
    label = scoreFont.render(text, 1, (255,0,0))
    screen.blit(label, (WINDOW_WIDTH-200, WINDOW_HEIGHT-40))
    
    clock.tick(fps)
    
    # Flip the display
    pygame.display.flip()
pygame.quit()
