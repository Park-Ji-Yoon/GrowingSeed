import pygame
import sys
from time import sleep


PAD_WIDTH = 800
PAD_HEIGHT = 650

def drawObject(object, x, y):
    global gamePad
    gamePad.blit(object, (x, y))

def initGame():
    global game_pad, clock, main_background, game_start_btn, game_rule_btn
    pygame.init()
    game_pad = pygame.display.set_mode((PAD_WIDTH, PAD_HEIGHT))
    pygame.display.set_caption("씨앗씨 키우기")
    main_background = pygame.image.load("imsi_1.png")
    game_start_btn = pygame.image.load("images/game_start_btn.png")
    game_rule_btn = pygame.image.load("images/game_rule_btn.png")
    clock = pygame.time.Clock()

def runGame():
    global game_pad, clock, main_background, game_start_btn, game_rule_btn

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

        drawObject(main_background, 0, 0)
        drawObject(game_start_btn, 430, 400)
        drawObject(game_rule_btn, 430, 500)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()