import math
import pygame

from lib import resources
from lib.utils import UP, DOWN, LEFT, RIGHT
from lib.animations import EntityAnimation
from lib.physics import WalkingDisplacement
from lib.ai import WandererBrain, DumbBrain
from lib.entities import Entity

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

    def __init__(self, origin, atkpos, *groups):
        super(Arrow, self).__init__('bullet', *groups)

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
