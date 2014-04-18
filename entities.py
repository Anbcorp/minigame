import math
import pygame
import random

import resources
import utils
from utils import DIRECTIONS, UP, DOWN, LEFT, RIGHT

class Bullet(pygame.sprite.Sprite):

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
        self.image = pygame.image.load(resources.getImage('bullet'))

        self.rect = origin
        self.speed = 700
        print atkpos, origin
        distance = math.sqrt(
                    math.pow(320 - atkpos[0], 2) +
                    math.pow(240 - atkpos[1], 2)
                    )
        self.direction_x = (atkpos[0] - 320)/distance
        self.direction_y = (atkpos[1] - 240)/distance
        print self.direction_x
        print self.direction_y

    def update(self, dt, game):
        self.rect.x += self.direction_x * self.speed * dt
        self.rect.y += self.direction_y * self.speed * dt

class WalkingEntity(pygame.sprite.Sprite):

    def __init__(self, name, *groups):
        super(WalkingEntity, self).__init__(*groups)
        self.tileset = pygame.image.load(resources.getImage(name))
        ## set sprites
        self.sprites = { 'up':[
                    self.tileset.subsurface(pygame.Rect(0,96,32,32)),
                    self.tileset.subsurface(pygame.Rect(32,96,32,32)),
                    self.tileset.subsurface(pygame.Rect(64,96,32,32)),
                    ],
                'down':[
                    self.tileset.subsurface(pygame.Rect(0,0,32,32)),
                    self.tileset.subsurface(pygame.Rect(32,0,32,32)),
                    self.tileset.subsurface(pygame.Rect(64,0,32,32)),
                    ],
                'left':[
                    self.tileset.subsurface(pygame.Rect(0,32,32,32)),
                    self.tileset.subsurface(pygame.Rect(32,32,32,32)),
                    self.tileset.subsurface(pygame.Rect(64,32,32,32)),
                    ],
                'right':[
                    self.tileset.subsurface(pygame.Rect(0,64,32,32)),
                    self.tileset.subsurface(pygame.Rect(32,64,32,32)),
                    self.tileset.subsurface(pygame.Rect(64,64,32,32)),
                    ],
                }
        self.image = self.sprites['right'][0]
        self.rect = pygame.rect.Rect(resources.getValue('%s.start' % name), (16,24))
        self.last = self.rect.copy()
        self.h_speed = resources.getValue('%s.speed' % name)
        self.v_speed = resources.getValue('%s.speed' % name)

        self.anim_dt = 0
        self.sprite_idx = 0

        self.direction = RIGHT

    def walk(self, dt):
       self.anim_dt += dt
       if self.anim_dt > 10./self.h_speed*2:
           self.sprite_idx = (self.sprite_idx+1)%3
           self.anim_dt = 0

    def think(self, dt, game):
        pass

    def update(self, dt, game):
        self.walk(dt)
        self.think(dt, game)

        # TODO: collbox is wrong
        for cell in pygame.sprite.spritecollide(self,
            game.current_level.blockers, False):
            self.rect = self.last
        self.last = self.rect.copy()





class Player(WalkingEntity):

    def __init__(self, *groups):
        super(Player, self).__init__('player', *groups)

        self.key_pressed = set()
        self.atks = []

    def think(self, dt, game):
        self.processInput(dt, game)

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

    def processInput(self, dt, game):
        atkpos = self.rect.copy()
        atkpos.x += 8
        atkpos.y += 10
        for key in self.key_pressed:
            if key == pygame.K_LEFT:
                self.rect.x -= self.h_speed * dt
                self.direction = LEFT
                self.image = self.sprites['left'][self.sprite_idx]
            if key == pygame.K_RIGHT:
                self.rect.x += self.h_speed * dt
                self.direction = RIGHT
                self.image = self.sprites['right'][self.sprite_idx]
            if key == pygame.K_UP:
                self.rect.y -= self.v_speed * dt
                self.direction = UP
                self.image = self.sprites['up'][self.sprite_idx]
            if key == pygame.K_DOWN:
                self.rect.y += self.h_speed * dt
                self.direction = DOWN
                self.image = self.sprites['down'][self.sprite_idx]

            if key == pygame.K_f:
                Bullet(self.direction, atkpos, game.entities)

        # process saved attacks directions and actually fire
        for pos in self.atks:
            Arrow(atkpos, pos, game.entities)
        self.atks = []

class Anima(WalkingEntity):

    def __init__(self, *groups):
        super(Anima, self).__init__('ork', *groups)

        self.time = 0
        self.direction = 0

    def think(self, dt, game):
        self.time += dt
        if self.time > random.randrange(1,15)/10.:
            self.direction = random.choice(DIRECTIONS)
            self.time = 0

        if self.direction == LEFT:
            self.rect.x -= self.h_speed * dt
            self.image = self.sprites['left'][self.sprite_idx]
        if self.direction == RIGHT:
            self.rect.x += self.h_speed * dt
            self.image = self.sprites['right'][self.sprite_idx]
        if self.direction == UP:
            self.rect.y -= self.v_speed * dt
            self.image = self.sprites['up'][self.sprite_idx]
        if self.direction == DOWN:
            self.rect.y += self.h_speed * dt
            self.image = self.sprites['down'][self.sprite_idx]

        for cell in pygame.sprite.spritecollide(self, game.entities, False):
            if isinstance(cell, Arrow) and not isinstance(cell, Player):
                cell.kill()
                self.kill()

class Ghosted(WalkingEntity):

    def __init__(self, *groups):
        super(Ghosted, self).__init__('ork', *groups)
        self.time = 0
        self.rect.x = 300
        self.rect.y = 200

    def think(self, dt, game):
        return
        self.time += dt
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.time > 0.1:
            #self.colors(dt, game)
            self.blend(dt, game)
            self.time = 0

    def blend(self, dt, game):
        self.image.fill((0,0,150,0), special_flags = pygame.BLEND_ADD)
        #self.image.blit(utils.BLUE, (0,0), special_flags = pygame.BLEND_RGB_ADD)

    def compare(self,dt, game):
       pxarray = pygame.PixelArray(self.image.copy())
       pxarray[0:-1] = 0

       px_image = pygame.PixelArray(self.image)

       npx = pxarray.compare(px_image, distance=.7)

       self.image = npx.make_surface()
       self.time = 0

    def colors(self, dt, game):
        pixs = pygame.PixelArray(self.image.copy())
        colmod = random.randint(0,255)
        for x in range(len(pixs)):
            for y in range(len(pixs)):
                    c = self.image.get_at((x, y))
                    (h,s,v,a) = c.hsva
                    hn = (h+60)%360

                    (c.r, c.g, c.b) = utils.hsv2rgb(hn,s,v)
                    self.image.set_at((x,y), c)
                    hp = c.hsva[0]
                    if x == 16 and y == 5:
                        print h, hn, hp

        print "done"
