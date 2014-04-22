import random

from lib.utils import DIRECTIONS, UP, DOWN, LEFT, RIGHT

class DumbBrain(object):
    def __init__(self, entity):
        self.entity = entity

    def touched_by(self, sprite):
        pass

    def think(self, delta_time, game):
        pass

class WandererBrain(DumbBrain):
    def __init__(self, entity):
        super(WandererBrain, self).__init__(entity)
        self.elapsed_time = 0

    def touched_by(self, sprite):
        self.change_direction()

    def change_direction(self):
        available_dirs = DIRECTIONS[:]
        available_dirs.pop(self.entity.direction)
        self.entity.direction = random.choice(available_dirs)

    def think(self, delta_time, game):
        # Work only on entities that can move
        if not self.entity.displacement :
            return

        self.elapsed_time += delta_time
        if self.elapsed_time > random.randrange(1,15)/10.:
            #self.entity.direction = random.choice(DIRECTIONS)
            self.elapsed_time = 0

        # Reset vector
        self.entity.vector = [0,0]
        if self.entity.direction == LEFT:
            self.entity.vector[0] = -self.entity.h_speed * delta_time

        if self.entity.direction == RIGHT:
            self.entity.vector[0] = +self.entity.h_speed * delta_time

        if self.entity.direction == UP:
            self.entity.vector[1] = -self.entity.v_speed * delta_time

        if self.entity.direction == DOWN:
            self.entity.vector[1] = +self.entity.v_speed * delta_time
