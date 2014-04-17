__author__ = 'Anb'

import pygame
import level
import resources

from entities import Player, Anima, Ghosted

from utils import *


class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        tiles = level.ScrolledGroup()
        tiles.camera_x = 0
        tiles.camera_y = 0

        # TODO: camera issues, or Z-level issues ?
        entities = pygame.sprite.Group()
        self.player = Player(entities)
        self.enemy = Ghosted(entities)
       # for i in range(0,100):
       #     Anima(sprites)

        self.current_level = level.Level()

        tiles.add(self.current_level.walls)
        tiles.add(self.current_level.tiles)

        while True:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                   event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                    ):
                    return

            entities.update(dt / 1000., self)
            # TODO : screen size constants
            tiles.camera_x = self.player.rect.x - 320
            tiles.camera_y = self.player.rect.y - 240
            screen.fill(RED)
            tiles.draw(screen)
            entities.draw(screen)

            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    # TODO : screen size from conf ? Or at least constant
    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)

    Game().main(screen)
