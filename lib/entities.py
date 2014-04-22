
import pygame

import resources
from utils import RIGHT


class Entity(pygame.sprite.Sprite):
    """
    Base class for entities
    """
    def __init__(self, name, *groups):
        super(Entity, self).__init__(*groups)
        self.animation = None
        self.brain = None
        self.displacement = None
        self.attack = None

        self.tileset = pygame.image.load(resources.getImage(name))
        self.direction = RIGHT

    @property
    def h_speed(self):
        if self.displacement:
            return self.displacement.h_speed
        return 0

    @property
    def v_speed(self):
        if self.displacement:
            return self.displacement.v_speed
        return 0

    @property
    def vector(self):
        if self.displacement:
            return self.displacement.vector
        return [0,0]
    @vector.setter
    def vector(self, vector):
        if self.displacement:
            if not isinstance(vector, list) or len(vector) < 2:
                raise ValueError('Vector is a two value list')
            self.displacement.vector = vector[0:2]

    def animate(self, delta_time, game):
        if self.animation:
            self.animation.animate(delta_time, game)

    def think(self, delta_time, game):
        if self.brain:
            self.brain.think(delta_time, game)

    def move(self, delta_time, game):
        if self.displacement:
            self.displacement.move(self.vector[0], self.vector[1],
                self.solid_objects)

    def fire_attack(self, delta_time, game):
        if self.attack:
            self.attack.fire_attack(self.target)

    def touched_by(self, entity):
        pass

    def update(self, delta_time, game):
        self.think(delta_time, game)
        self.animate(delta_time, game)
        self.move(delta_time, game)
        self.fire_attack(delta_time, game)
