__author__ = 'Anb'

import pygame

from utils import *


class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()
        color = BLUE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                   event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                    ):
                    return
            clock.tick(30)
            screen.fill(color)
            if color is BLUE:
                color = RED
            else:
                color = BLUE

            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)

    Game().main(screen)
