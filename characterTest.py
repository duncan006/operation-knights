import sys
import random
import pygame
import characterClass
pygame.init()

fps = 30
WINDOW_HEIGHT = 300
WINDOW_WIDTH = 600

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
player = Player(WINDOW_WIDTH/2,WINDOW_HEIGHT-50,(255,0,0))
clock = pygame.time.Clock()

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
    
    clock.tick(fps)
    
    pygame.display.flip()
pygame.quit()
