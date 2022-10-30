import pygame, sys
from datafile import *
from pygame.locals import *

clock = pygame.time.Clock()

screenSize = (400, 400) # 창 크기
gameScreen = pygame.display.set_mode(screenSize)    # 창모드
pygame.display.set_caption('Roguelike!')    # 게임 이름 표시
pygame.init()

spr_character = SpriteUpscaling('test.png', 16, 16, 8, 8, 11)
gameScreen.fill("white")

while True:
    gameScreen.blit(spr_character.spr[0], (174, 174)) # 화면 그리기 (스프라이트, 위치)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update() # 화면 업데이트 
    clock.tick(60)