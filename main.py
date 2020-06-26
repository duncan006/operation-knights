import sys
import pygame
import random

pygame.init()

spawnRate = 1000

WIDTH = 800
HEIGHT = 600

P_COLOR = (255, 0, 0)
P_SIZE = 50
P_POS = [WIDTH/3, HEIGHT-P_SIZE]
P_SPEED = 20

E_COLOR = (0, 0, 255)
E_SIZE = 50
E_POS = [random.randint(0, WIDTH-E_SIZE),0]
E_SPEED = 10
enemyList = []

background_color = (0,0,0)
gravity = 15
game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

screen = pygame.display.set_mode((WIDTH,HEIGHT))

def drop_enemies(enemyList):
    if random.random() <= .1:
        if len(enemyList) < 10:
            x_pos = random.randint(0,WIDTH-E_SIZE)
            y_pos = 0
            enemyList.append([x_pos, y_pos])
        
def draw_enemies(enemyList):
    for enemyPos in enemyList:
        pygame.draw.rect(screen, E_COLOR, (enemyPos[0],enemyPos[1],E_SIZE,E_SIZE))

def update_enemy_pos(enemyList, score):
    for idx, enemyPos in enumerate(enemyList):
        if enemyPos[1] >= 0 and enemyPos[1] < HEIGHT:
            enemyPos[1] += E_SPEED
        else:
            enemyList.pop(idx)
            score += 1
    return score

def enemy_collision_check(enemyList, playerPos):
    for enemyPos in enemyList:
        if collision_handler(enemyPos, playerPos):
            return True
    return False

def collision_handler(p_pos, e_pos):
    px = p_pos[0]
    py = p_pos[1]
    ex = e_pos[0]
    ey = e_pos[1]
    
    if (ex >= px and ex < (px + P_SIZE)) or ((px >= ex and px < (ex + E_SIZE))):
        if (ey >= py and ey < (py + P_SIZE)) or ((py >= ey and py < (ey + E_SIZE))):
            return True
    return False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            x = P_POS[0]
            y = P_POS[1]
            if event.key == pygame.K_a:
                x -= P_SPEED
            elif event.key == pygame.K_d:
                x += P_SPEED
            elif event.key == pygame.K_w:
                pass  
            P_POS = [x,y]
    
    
    screen.fill(background_color)

    drop_enemies(enemyList)
    score = update_enemy_pos(enemyList, score)
    
    if enemy_collision_check(enemyList, P_POS) == True:
        game_over = True
        break
    
    draw_enemies(enemyList)
    
    text = "score: " + str(score)
    label = myFont.render(text, 1, (255,0,0))
    screen.blit(label, (WIDTH-200, HEIGHT-40))
    pygame.draw.rect(screen, P_COLOR, (P_POS[0],P_POS[1],P_SIZE,P_SIZE))
    
    clock.tick(30)
    
    pygame.display.update()
