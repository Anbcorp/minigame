import math
import pygame
import random

import resources
from utils import DIRECTIONS, UP, DOWN, LEFT, RIGHT

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

class Arrow(pygame.sprite.Sprite):
    """
    A projectile with an origin and an attack target used to compute its
    direction
    """

    def __init__(self, origin, atkpos, *groups):
        super(Arrow, self).__init__(*groups)
        self.image = pygame.image.load("res/bullet.png")

        self.rect = pygame.Rect((origin.x, origin.y), (16, 16))
        self.speed = 300
        print atkpos, origin
        distance = math.sqrt(
                    math.pow(320 - atkpos[0], 2) +
                    math.pow(240 - atkpos[1], 2)
                    )
        self.direction_x = (atkpos[0] - 320)/distance
        self.direction_y = (atkpos[1] - 240)/distance
        print self.direction_x
        print self.direction_y

        self.solid = True

    def update(self, dt, game):
        self.last = self.rect.copy()

        vector = (
            self.direction_x * self.speed * dt,
            self.direction_y * self.speed * dt,
            )

        self.move(vector, game)

    def move(self, vector, game):
        vx = vector[0]
        vy = vector[1]
        # We are forced to split the collision problem in two composant
        if vx != 0 or vy != 0 :
            if vx != 0 :
                self.rect.x += vx
                self.collide(vx, 0, game)
            if vy != 0 :
                self.rect.y += vy
                self.collide(0, vy, game)

    def collide(self, vx, vy, game):
        if vx != 0 and vy != 0 :
            raise ValueError()

        sprite = None
        topbottom = False
        leftright = False
        for sprite in pygame.sprite.spritecollide(self, game.current_level.blockers, False, pygame.sprite.collide_rect):

            if  self.rect.x < (sprite.rect.right + self.last.width) and \
                self.rect.x > (sprite.rect.left - self.last.width) and \
                vx == 0\
                :
                topbottom = True

            if  self.rect.y > (sprite.rect.top - self.last.height) and \
                self.rect.y < (sprite.rect.bottom + self.last.height) and\
                vy == 0\
                :
                leftright = True

            if not (topbottom or leftright) :
                return
            if topbottom and leftright:
                print "BOOG"

        if topbottom :
            self.direction_y *= -1
            if vy > 0:
                self.rect.bottom = sprite.rect.top - 1
            if vy < 0:
                self.rect.top = sprite.rect.bottom + 1
        if leftright :
            self.direction_x *= -1
            if vx > 0:
                self.rect.right = sprite.rect.left - 1
            if vx < 0:
                self.rect.left = sprite.rect.right + 1

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
            self.animation.animate(delta_time)

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

class Enemy(Entity):

    def __init__(self, name, *groups):
        super(Enemy, self).__init__(name, *groups)

        self.animation = EntityAnimation(self)
        self.displacement = WalkingDisplacement(self)
        self.displacement.set_speed(resources.getValue('%s.speed' % name))
        self.brain = WandererBrain(self)

    def move(self, delta_time, game):
        self.displacement.move(self.vector[0], self.vector[1],
            game.current_level.blockers)

    def touched_by(self, sprite):
        if sprite and self.brain:
            self.brain.touched_by(sprite)

class EntityAnimation(object):
    def __init__(self, entity):
        # define sprites here
        self.entity = entity
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

    def animate(self, delta_time):
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

class Displacement(object):
    """
    Define the path to take when moving

    And how to react to collisions
    """

    def __init__(self, entity):
        self.entity = entity
        self.h_speed = 200
        self.v_speed = 200
        self.vector = [0,0]

    def set_speed(self, speed):
        self.h_speed = speed
        self.v_speed = speed

    def move(self, xoffset, yoffset, colliding_sprites):
        pass

class WalkingDisplacement(Displacement):
    def __init__(self, entity):
        super(WalkingDisplacement, self).__init__(entity)


    def move(self, xoffset, yoffset, colliding_sprites):
        """
        Move the entity using the provided displacements and check collision
        with colliding_sprites group

        Returns a list of sprite we collided with
        """
        # We are forced to split the collision problem in two composant
        collided_sprites = []
        if xoffset != 0 or yoffset != 0 :
            if xoffset != 0 :
                self.entity.rect.x += xoffset
                collided_sprites = self.collide(xoffset, 0, colliding_sprites)
            if yoffset != 0 :
                self.entity.rect.y += yoffset
                collided_sprites += self.collide(0, yoffset, colliding_sprites)

        # Launch callbacks for touched sprites
        for sprite in collided_sprites :
            self.entity.touched_by(sprite)

    def collide(self, xoffset, yoffset, colliding_sprites):
        """
        Check if the entity collided with the provided spritegroup

        We use the xoffset and yoffset values for some advanced detection

        Return a list of sprites colliding with self.entity
        """
        # utility vars
        entity = self.entity

        if xoffset != 0 and yoffset != 0 :
            raise ValueError()

        sprite = None
        topbottom = False
        leftright = False
        collided_sprites = pygame.sprite.spritecollide(entity,
            colliding_sprites,
            False,
            pygame.sprite.collide_rect)

        for sprite in collided_sprites:
            if  entity.rect.x < (sprite.rect.right + entity.rect.width) and \
                entity.rect.x > (sprite.rect.left - entity.rect.width) and \
                xoffset == 0\
                :
                topbottom = True

            if  entity.rect.y > (sprite.rect.top - entity.rect.height) and \
                entity.rect.y < (sprite.rect.bottom + entity.rect.height) and\
                yoffset == 0\
                :
                leftright = True

            if not (topbottom or leftright) :
                # not really a collision
                return []
            if topbottom and leftright:
                print "BOOG"


            self.collision_react(sprite, topbottom, leftright, xoffset, yoffset)

        return collided_sprites

    def collision_react(self, sprite, topbottom, leftright, xoffset, yoffset):
        """
        This is where collision reaction happen (rebound, glue, passthrough in
        certain cases)

        Entities interactions (hit, knockback) should be handled by
        Entity.touched_by(entity)
        """
        if topbottom :
            self.entity.vector[1] *= -0
            if yoffset > 0:
                self.entity.rect.bottom = sprite.rect.top - 1
            if yoffset < 0:
                self.entity.rect.top = sprite.rect.bottom + 1
        if leftright :
            self.entity.vector[0] *= -0
            if xoffset > 0:
                self.entity.rect.right = sprite.rect.left - 1
            if xoffset < 0:
                self.entity.rect.left = sprite.rect.right + 1

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
            Arrow(atkpos, pos, game.entities)
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

        self.displacement = WalkingDisplacement(self)
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
