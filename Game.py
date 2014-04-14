__author__ = 'Anb'

import pygame
import level
import resources

from entities import Player

from utils import *


class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        sprites = level.ScrolledGroup()
        sprites.camera_x = 0
        sprites.camera_y = 0
        self.player = Player(sprites)

        self.current_level = level.Level()

        sprites.add(self.current_level.walls)

        while True:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                   event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                    ):
                    return

            sprites.update(dt / 1000., self)
            screen.fill(RED)
            sprites.draw(screen)

            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    # TODO : screen size from conf ? Or at least constant
    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)

    Game().main(screen)
