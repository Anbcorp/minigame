__author__ = 'Anbcorp'

import pygame

import resources

class ScrolledGroup(pygame.sprite.Group):
    """
    This is a sprite Group() whose drawn surface is controlled by camera position

    This suppose all sprites for the level are kept in memory
    """
    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y - self.camera_y))

class Level(object):
    """
    Basic level object
    """
    def __init__(self):
        self.walls = pygame.sprite.Group()

        (self.h_size, self.v_size) = resources.getValue('level.size')
        # TODO: howto load a tile ?
        block = pygame.image.load(resources.getImage('block'))
        # TODO: level generation here
        # TODO: arbitrary level sizes do not work (empty wall) is not a multiple of 32
        for x in range(0, self.h_size, 32):
            for y in range(0,self.v_size,32):
                if x in (0,self.h_size-32) or y in (0, self.v_size-32):
                    # Sprite(*groups) add the new sprites in the groups
                    wall = pygame.sprite.Sprite(self.walls)
                    wall.image = block
                    wall.rect = pygame.rect.Rect((x,y), block.get_size())
