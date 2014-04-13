__author__ = 'Anb'

import pygame
import resources

from Player import Player

from utils import *


class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        sprites = pygame.sprite.Group()
        self.player = Player(sprites)

        # TODO: howto load a tile ?
        block = pygame.image.load(resources.getImage('block'))
        self.walls = pygame.sprite.Group()

        # TODO: level generation here
        for x in range(0, 640, 32):
            for y in range(0,480,32):
                if x in (0,640-32) or y in (0, 480-32):
                    wall = pygame.sprite.Sprite(self.walls)
                    wall.image = block
                    wall.rect = pygame.rect.Rect((x,y), block.get_size())
        sprites.add(self.walls)

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
    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)

    Game().main(screen)
