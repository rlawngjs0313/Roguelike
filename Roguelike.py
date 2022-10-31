import pygame
from datafile import *
from pygame.locals import *

clock = pygame.time.Clock()
screenSize = (1000, 1000) # 창 크기
gameScreen = pygame.display.set_mode(screenSize)    # 창모드
pygame.display.set_caption('Roguelike!')    # 게임 이름 표시
pygame.init()
print("D")

spr_character = SpriteUpscaling('test.png', 16, 16, 8, 8, 11)
gameScreen.fill((255, 255, 255))

player_x = screenSize[0] / 2
player_y = screenSize[1] / 2
dy = 0
dx = 0
speed = 10

running = True 
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN: # 움직임 파트
            if event.key == pygame.K_w:
                dy -= speed
            elif event.key == pygame.K_a:
                dx -= speed
            elif event.key == pygame.K_s:
                dy += speed
            elif event.key == pygame.K_d:
                dx += speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                dy = 0
            elif event.key == pygame.K_a:
                dx = 0
            elif event.key == pygame.K_s:
                dy = 0
            elif event.key == pygame.K_d:
                dx = 0
        
    player_x += dx
    player_y += dy
    gameScreen.fill((255,255,255))
    gameScreen.blit(spr_character.spr[0], (player_x, player_y))
    pygame.display.flip()
    clock.tick(60)