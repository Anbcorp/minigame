__author__ = 'Anbcorp'

import numpy
import pygame
import random

from lib import resources
from lib.utils import DIRECTIONS, DOWN, LEFT, RIGHT, UP

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
        self.start_pos = pygame.Rect(64,64,0,0)

        self.generate()


    def generate(self):
        raise RuntimeError('not implemented')

    def update(self, dt, game):
        self.tiles.update(dt, game)
        self.blockers.update(dt, game)

    def draw(self, screen):
        self.tiles.draw(screen)
        self.blockers.draw(screen)


class BasicLevel(Level):

    def __init__(self):
        super(BasicLevel, self).__init__()

    def generate(self):
        # we use pixels instead of tiles
        self.h_size *= 32
        self.v_size *= 32
        tiles = pygame.image.load(resources.getImage('level'))
        # TODO: load a specific tile from resources
        block = tiles.subsurface(pygame.Rect(6*32,3*32,32,32))

        grass = tiles.subsurface(pygame.Rect(0,0,32,32))
        print block.get_size()
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


class MazeLevel(Level):

    def __init__(self):
        super(MazeLevel, self).__init__()

        self.blockers

    def generate(self):
        h_size = self.h_size
        v_size = self.v_size
        def getTile(x,y,size=16):
            return tiles.subsurface(pygame.Rect(x*16,y*16,16,16))

        tiles = pygame.image.load(resources.getImage('level'))
        # TODO: load a specific tile from resources
        block = tiles.subsurface(pygame.Rect(64,192,32,32))
        blocks = {
            'N1':getTile(5,14),
            'N2':getTile(6,14),
            'S1':getTile(5,17),
            'S2':getTile(6,17),
            'E1':getTile(7,15),
            'E2':getTile(7,16),
            'W1':getTile(4,15),
            'W2':getTile(4,16),
            'NW':getTile(4,14),
            'NE':getTile(7,14),
            'SW':getTile(4,17),
            'SE':getTile(7,17),
            'mNW':getTile(5,15),
            'mNE':getTile(6,15),
            'mSW':getTile(5,16),
            'mSE':getTile(6,16),
        }
        grass = tiles.subsurface(pygame.Rect(0,0,32,32))

        level = numpy.zeros((h_size, v_size))

        pos = [
            random.randint(1, h_size - 2),
            random.randint(1, v_size - 2)
            ]
        self.start_pos = pygame.Rect(pos[0]*32, pos[1]*32, 0, 0)

        self.start_dir = random.choice(DIRECTIONS)
        dire = self.start_dir

        level[pos[0],pos[1]] = 1
        for i in range(0,50):
            for step in range(4,random.randint(5,25)):
                if dire == UP:
                    pos[1] -= 1
                    if pos[1] < 1 :
                        pos[1] = 1
                        dire = random.choice((DOWN,LEFT,RIGHT))

                if dire == DOWN:
                    pos[1] += 1
                    if pos[1] > v_size - 2:
                        pos[1] = v_size- 2
                        dire = random.choice((LEFT,RIGHT,UP))

                if dire == LEFT:
                    pos[0] += 1
                    if pos[0] > h_size - 2:
                        pos[0] = h_size - 2
                        dire = random.choice((DOWN,RIGHT,UP))

                if dire == RIGHT:
                    pos[0] -= 1
                    if pos[0] < 1:
                        pos[0] = 1
                        dire = random.choice((DOWN,LEFT,UP))

                level[pos[0],pos[1]] = 1
            choices = DIRECTIONS[:]
            choices.pop(dire)
            dire = random.choice(choices)
        print "map ok"
        for y in range(0, v_size):
            for x in range(0, h_size):
                if level[x,y] == 0:
                    # place tiles according to surroundings
                    # the resulting surface is 32x32
                    wall = pygame.sprite.Sprite(self.blockers)
                    wall.image = pygame.Surface((32,32))
                    # get value for 8 tiles surroundings
                    def get_adj_tile(x, y):
                        if x > h_size-1 or x < 0 :
                            return 0
                        if y > v_size-1 or y < 0 :
                            return 0
                        return int(level[x,y])

                    n  = int(get_adj_tile(x,y-1))   << 0
                    ne = int(get_adj_tile(x+1,y-1)) << 1
                    e  = int(get_adj_tile(x+1,y))   << 2
                    se = int(get_adj_tile(x+1,y+1)) << 3
                    s  = int(get_adj_tile(x,y+1))   << 4
                    sw = int(get_adj_tile(x-1,y+1)) << 5
                    w  = int(get_adj_tile(x-1,y))   << 6
                    nw = int(get_adj_tile(x-1,y-1)) << 7

                    v = n+s+e+w+nw+ne+sw+se
                    # Assign a bit for each tile surrounding
                    # | 128 |   1 |   2 |
                    # |  64 | til |   4 |
                    # |  32 |  16 |   8 |
                    #
                    # then for each quadrant of our tile, we have four cases
                    # (the fifth if redundant) these cases wille be represented
                    # by values, obtained by masking bits
                    qNW = v & 0b11000001
                    qNE = v & 0b00000111
                    qSE = v & 0b00011100
                    qSW = v & 0b01110000

                    # for the NW quadrant (x is our tile, O is empty, X is
                    # filled)
                    if qNW == 193:
                        # OO
                        # Ox
                        tNW = blocks['NW']
                    elif qNW == 129:
                        # OO
                        # Xx
                        tNW = blocks['N1']
                    elif qNW == 192:
                        # XO
                        # Xx
                        tNW = blocks['W1']
                    else:
                        # XX
                        # Xx
                        tNW = blocks['mNW']

                    if qNE == 7:
                        # 111
                        # OO
                        # xO
                        tNE = blocks['NE']
                    elif qNE == 3:
                        # OO
                        # xX
                        tNE = blocks['N2']
                    elif qNE == 6:
                        # XO
                        # xX
                        tNE = blocks['E1']
                    else:
                        # XX
                        # xX
                        tNE = blocks['mNE']

                    if qSE == 28:
                        # 111
                        # xO
                        # OO
                        tSE = blocks['SE']
                    elif qSE == 12:
                        # xO
                        # XO
                        tSE = blocks['E2']
                    elif qSE == 24:
                        # xX
                        # OO
                        tSE = blocks['S2']
                    else:
                        # xX
                        # XX
                        tSE = blocks['mSE']

                    if qSW == 112:
                        # 111
                        # Ox
                        # OO
                        tSW = blocks['SW']
                    elif qSW == 48:
                        # Xx
                        # OO
                        tSW = blocks['S1']
                    elif qSW == 96:
                        # Ox
                        # OX
                        tSW = blocks['W2']
                    else:
                        # Xx
                        # XX
                        tSW = blocks['mSW']

                    # We blit the smaller tiles into a larger one
                    wall.image.blit(tNW, (0,0))
                    wall.image.blit(tNE, (16,0))
                    wall.image.blit(tSE, (16,16))
                    wall.image.blit(tSW, (0,16))
                    wall.rect = pygame.rect.Rect((x*32,y*32), (32,32))
                else:
                    tile = pygame.sprite.Sprite(self.tiles)
                    tile.image = grass
                    tile.rect = pygame.rect.Rect((x*32,y*32), grass.get_size())

if __name__ == '__main__':
    m = MazeLevel()
