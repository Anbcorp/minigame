__author__ = 'Anbcorp'

import numpy
import pygame
import random

import resources
from utils import DIRECTIONS, DOWN, LEFT, RIGHT, UP

class ScrolledGroup(pygame.sprite.Group):
    """
    This is a sprite Group() whose drawn surface is controlled by camera position

    This suppose all sprites for the level are kept in memory
    """

    def __init__(self, *sprites):
        super(ScrolledGroup, self).__init__(*sprites)
        self._camera_x = 0
        self._camera_y = 0

    @property
    def camera(self):
        return (self._camera_x, self._camera_y)
    @camera.setter
    def camera(self, value):
        self._camera_x = value[0]
        self._camera_y = value[1]

    def update(self, dt, game, *args):
        super(ScrolledGroup, self).update(dt, game, *args)
        # TODO : screen size constants
        self.camera = (game.player.rect.x - 320, game.player.rect.y - 240)

    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, (
                sprite.rect.x - self._camera_x,
                sprite.rect.y - self._camera_y)
            )

class Level(object):
    """
    Basic level object
    """
    def __init__(self):
        self.blockers = ScrolledGroup()
        self.tiles = ScrolledGroup()

        (self.h_size, self.v_size) = resources.getValue('level.size')
        self.h_size *= 32
        self.v_size *= 32

        self.generate()
        self.start_pos = pygame.Rect(64,64,0,0)

    def generate(self):
        tiles = pygame.image.load(resources.getImage('level'))
        # TODO: load a specific tile from resources
        block = tiles.subsurface(pygame.Rect(64,192,32,32))
        grass = tiles.subsurface(pygame.Rect(0,0,32,32))
        # TODO: level generation here
        # TODO: arbitrary level sizes do not work (empty wall) is not a multiple of 32
        for x in range(0, self.h_size, 32):
            for y in range(0,self.v_size,32):
                if x in (0,self.h_size-32) or y in (0, self.v_size-32):
                    # Sprite(*groups) add the new sprites in the groups
                    wall = pygame.sprite.Sprite(self.blockers)
                    wall.image = block
                    wall.rect = pygame.rect.Rect((x,y), block.get_size())
                else:
                    if random.randint(0,12) == 0:
                        tile = pygame.sprite.Sprite(self.blockers)
                        tile.image = block
                    else:
                        tile = pygame.sprite.Sprite(self.tiles)
                        tile.image = grass
                    tile.rect = pygame.rect.Rect((x,y), tile.image.get_size())

    def update(self, dt, game):
        self.tiles.update(dt, game)
        self.blockers.update(dt, game)

    def draw(self, screen):
        self.tiles.draw(screen)
        self.blockers.draw(screen)

class MazeLevel(Level):

    def __init__(self):
        super(MazeLevel, self).__init__()

    def generate(self):
        tiles = pygame.image.load(resources.getImage('level'))
        # TODO: load a specific tile from resources
        block = tiles.subsurface(pygame.Rect(64,192,32,32))
        grass = tiles.subsurface(pygame.Rect(0,0,32,32))

        level = numpy.zeros((self.h_size, self.v_size))

        pos = [
            random.randint(0, self.h_size - 1),
            random.randint(0, self.v_size - 1)
            ]
        self.start_pos = pygame.Rect(pos[0]*32, pos[1]*32, 0, 0)

        self.start_dir = random.choice(DIRECTIONS)
        dire = self.start_dir

        level[pos[0],pos[1]] = 1
        for i in range(0,50):
            for step in range(4,random.randint(5,25)):
                if dire == UP:
                    pos[1] -= 1
                    if pos[1] < 0 :
                        pos[1] = 0
                        dire = random.choice((DOWN,LEFT,RIGHT))

                if dire == DOWN:
                    pos[1] += 1
                    if pos[1] > self.v_size - 1:
                        pos[1] = self.v_size- 1
                        dire = random.choice((LEFT,RIGHT,UP))

                if dire == LEFT:
                    pos[0] += 1
                    if pos[0] > self.h_size - 1:
                        pos[0] = self.h_size - 1
                        dire = random.choice((DOWN,RIGHT,UP))

                if dire == RIGHT:
                    pos[0] -= 1
                    if pos[0] < 0:
                        pos[0] = 0
                        dire = random.choice((DOWN,LEFT,UP))

                level[pos[0],pos[1]] = 1
            choices = DIRECTIONS[:]
            choices.pop(dire)
            dire = random.choice(choices)
        print "map ok"
        for y in range(0, self.v_size):
            for x in range(0, self.h_size):
                if level[x,y] == 0:
                    wall = pygame.sprite.Sprite(self.blockers)
                    wall.image = block
                    wall.rect = pygame.rect.Rect((x*32,y*32), block.get_size())
                else:
                    tile = pygame.sprite.Sprite(self.tiles)
                    tile.image = grass
                    tile.rect = pygame.rect.Rect((x*32,y*32), grass.get_size())

if __name__ == '__main__':
    m = MazeLevel()
