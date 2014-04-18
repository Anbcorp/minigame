__author__ = 'Anb'

import pygame
import level
import resources

from entities import Player, Anima, Ghosted, Bullet

from utils import *


class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        tiles = level.ScrolledGroup()

        self.current_level = level.Level()
        tiles.add(self.current_level.blockers)
        tiles.add(self.current_level.tiles)

        entities = level.ScrolledGroup()
        self.entities = entities
        self.player = Player(entities)

        for i in range(0,1000):
            Anima(entities)
#        self.enemy = Ghosted(entities)



        while True:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                   event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                    ):
                    return

            entities.update(dt / 1000., self)
            tiles.update(dt / 1000., self)
            screen.fill(RED)
            tiles.draw(screen)
            entities.draw(screen)

            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    # TODO : screen size from conf ? Or at least constant
    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)

    Game().main(screen)
