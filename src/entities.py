import math
import pygame

from lib import resources
from lib.utils import UP, DOWN, LEFT, RIGHT
from lib.animations import EntityAnimation, StaticAnimation
from lib.physics import BaseDisplacement, ReboundDisplacement
from lib.ai import WandererBrain, DumbBrain
from lib.entities import Entity
from lib.sounds import SoundFx

class Bullet(pygame.sprite.Sprite):
    """
    Bullets going straight once launched
    """
    def __init__(self, direction, firepos, *groups):
        super(Bullet, self).__init__(*groups)
        self.image = pygame.image.load(resources.getImage('bullet'))

        self.rect = firepos
        self.direction = direction
        self.speed = 800

    def update(self, dt, game):

        if self.direction == LEFT:
            self.rect.x -= self.speed * dt
        if self.direction == RIGHT:
            self.rect.x += self.speed * dt
        if self.direction == UP:
            self.rect.y -= self.speed * dt
        if self.direction == DOWN:
            self.rect.y += self.speed * dt

class Arrow(Entity):
    """
    A projectile with an origin and an attack target used to compute its
    direction
    """

    def __init__(self, origin, atkpos, game, *groups):
        super(Arrow, self).__init__('bullet', *groups)

        self.animation = StaticAnimation(self)
        self.displacement = ReboundDisplacement(self)
        self.displacement.set_speed(300)

        self.rect = pygame.Rect((origin.x, origin.y), (16, 16))

        self.solid_objects = game.current_level.blockers

        distance = math.sqrt(
                    math.pow(320 - atkpos[0], 2) +
                    math.pow(240 - atkpos[1], 2)
                    )

        self.vector = [
            (atkpos[0] - 320)/distance * self.displacement.h_speed,
            (atkpos[1] - 240)/distance * self.displacement.v_speed,
            ]

        self.sound_fx = SoundFx('bullet')

    def move(self, delta_time, game):
        vector = self.vector[:]
        vector[0] *= delta_time
        vector[1] *= delta_time
        self.displacement.move(vector[0], vector[1], self.solid_objects)

    def touched_by(self, entities):
        self.sound_fx.play_sound('hit')

class Enemy(Entity):

    def __init__(self, name, *groups):
        super(Enemy, self).__init__(name, *groups)

        self.animation = EntityAnimation(self)
        self.displacement = BaseDisplacement(self)
        self.displacement.set_speed(resources.getValue('%s.speed' % name))
        self.brain = WandererBrain(self)

    def move(self, delta_time, game):
        self.displacement.move(self.vector[0], self.vector[1],
            game.current_level.blockers)

    def touched_by(self, sprite):
        if sprite and self.brain:
            self.brain.touched_by(sprite)

class PlayerControlledBrain(DumbBrain):

    def __init__(self, entity):
        super(PlayerControlledBrain, self).__init__(entity)

        self.key_pressed = set()
        self.atks = []

    def think(self, delta_time, game):
        self.processInput(delta_time, game)

    def process_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_pressed.add(event.key)
        if event.type == pygame.KEYUP:
            # Sometime we release a key that was pressed out of game. Ignore
            # that
            try:
                self.key_pressed.remove(event.key)
            except KeyError:
                pass

    def process_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 :
                # enqueue attack directions in case of the player clicks faster
                # than the game can process
                self.atks.append(event.pos)

    def processInput(self, delta_time, game):
        atkpos = self.entity.rect.copy()
        atkpos.x += 8
        atkpos.y += 10
        self.entity.vector = [0,0]
        for key in self.key_pressed:
            if key == pygame.K_LEFT:
                self.entity.vector[0] = -self.entity.h_speed * delta_time
                self.entity.direction = LEFT
            if key == pygame.K_RIGHT:
                self.entity.vector[0] = +self.entity.h_speed * delta_time
                self.entity.direction = RIGHT
            if key == pygame.K_UP:
                self.entity.vector[1] = -self.entity.h_speed * delta_time
                self.entity.direction = UP
            if key == pygame.K_DOWN:
                self.entity.vector[1] = +self.entity.v_speed * delta_time
                self.entity.direction = DOWN

        # process saved attacks directions and actually fire
        for pos in self.atks:
            Arrow(atkpos, pos, game, game.entities)
        self.atks = []

class Player(Entity):

    def __init__(self, game, *groups):
        super(Player, self).__init__('player', *groups)

        self.brain = PlayerControlledBrain(self)
        game.event_listener.register_listener(self.brain, pygame.KEYDOWN)
        game.event_listener.register_listener(self.brain,
            pygame.MOUSEBUTTONDOWN)

        self.animation = EntityAnimation(self)
        self.rect = pygame.Rect((0,0), (16,24))

        self.displacement = BaseDisplacement(self)
        self.displacement.set_speed(resources.getValue('%s.speed' % 'player'))

    def move_to(self, new_position):
        if isinstance(new_position, list) or isinstance(new_position, tuple):
            self.rect.x = new_position[0]
            self.rect.y = new_position[1]
        elif isinstance(new_position, pygame.Rect):
            self.rect.x = new_position.x
            self.rect.y = new_position.y
        else:
            raise ValueError("%s.move_to " % (self.__class__) +
                "takes a tuple of coordinates (x,y) or a Rect()")

    def move(self, delta_time, game):
        self.displacement.move(self.vector[0], self.vector[1],
            game.current_level.blockers)
