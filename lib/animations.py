import pygame

from utils import UP, DOWN, LEFT, RIGHT


class Animation(object):

    def __init__(self, entity):
        self.entity = entity

    def animate(self, delta_time, game):
        pass

class StaticAnimation(Animation):
    """
    Mockup to handle non animated objects

    Use the tileset as the single animation frame.
    """
    def __init__(self, entity):
        super(StaticAnimation, self).__init__(entity)
        self.entity.image = self.entity.tileset

class EntityAnimation(Animation):
    """
    Animates entity or anything that have 4 animations (one per direction) of 3
    frames each
    """
    def __init__(self, entity):
        super(EntityAnimation, self).__init__(entity)
        # TODO: handles more (or less) than three frames per animation
        self.sprites = {
                'up':[
                    entity.tileset.subsurface(pygame.Rect(0,96,32,32)),
                    entity.tileset.subsurface(pygame.Rect(32,96,32,32)),
                    entity.tileset.subsurface(pygame.Rect(64,96,32,32)),
                    ],
                'down':[
                    entity.tileset.subsurface(pygame.Rect(0,0,32,32)),
                    entity.tileset.subsurface(pygame.Rect(32,0,32,32)),
                    entity.tileset.subsurface(pygame.Rect(64,0,32,32)),
                    ],
                'left':[
                    entity.tileset.subsurface(pygame.Rect(0,32,32,32)),
                    entity.tileset.subsurface(pygame.Rect(32,32,32,32)),
                    entity.tileset.subsurface(pygame.Rect(64,32,32,32)),
                    ],
                'right':[
                    entity.tileset.subsurface(pygame.Rect(0,64,32,32)),
                    entity.tileset.subsurface(pygame.Rect(32,64,32,32)),
                    entity.tileset.subsurface(pygame.Rect(64,64,32,32)),
                    ],
                }
        self.elapsed_time = 0
        self.frame = 0

        self.entity.image = self.sprites['right'][0]

    def animate(self, delta_time, game):
        speed = self.entity.h_speed
        self.elapsed_time += delta_time

        # Do not animate if entity have no speed or is not moving
        if speed == 0 :
            return
        if self.entity.vector[0] == 0 and self.entity.vector[1] == 0:
            return

        if self.elapsed_time > 10./speed*2:
            self.frame = (self.frame+1)%3
            self.elapsed_time = 0

        if self.entity.direction == LEFT:
            self.entity.image = self.sprites['left'][self.frame]
        if self.entity.direction == RIGHT:
            self.entity.image = self.sprites['right'][self.frame]
        if self.entity.direction == UP:
            self.entity.image = self.sprites['up'][self.frame]
        if self.entity.direction == DOWN:
            self.entity.image = self.sprites['down'][self.frame]
