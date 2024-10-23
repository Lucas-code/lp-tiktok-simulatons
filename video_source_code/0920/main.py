import pygame

from Game import Game
from Utils import utils

game = Game()

while True:
    utils.screen.fill((23, 23, 23), (0, 0, utils.width, utils.height))
    utils.initDeltaTime()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    if game.isActive:
        game.update()
    game.draw()


    pygame.display.flip()