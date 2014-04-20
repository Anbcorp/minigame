import pygame

class Movement(object):
    """
    Base class for movements
    """

    def __init__(self, game, entity):
        self.entity = entity
        self.game = game
        print id(self.game)
        self.solid_sprites = self.game.current_level.blockers

    def move(self, xoffset, yoffset):
        """
        Move the entity using the provided displacements

        Returns a list of sprite we collided with
        """
        # We are forced to split the collision problem in two composant
        if xoffset != 0 or yoffset != 0 :
            if xoffset != 0 :
                self.entity.rect.x += xoffset
                colliding_sprites = self.collide(xoffset, 0)
            if yoffset != 0 :
                self.entity.rect.y += yoffset
                colliding_sprites += self.collide(0, yoffset)

    def collide(self, xoffset, yoffset):
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
        colliding_sprites = pygame.sprite.spritecollide(entity,
            self.solid_sprites,
            False,
            pygame.sprite.collide_rect)

        for sprite in colliding_sprites:
            if  entity.rect.x < (sprite.rect.right + entity.last.width) and \
                entity.rect.x > (sprite.rect.left - entity.last.width) and \
                xoffset == 0\
                :
                topbottom = True

            if  entity.rect.y > (sprite.rect.top - entity.last.height) and \
                entity.rect.y < (sprite.rect.bottom + entity.last.height) and\
                yoffset == 0\
                :
                leftright = True

            if not (topbottom or leftright) :
                # not really a collision
                return []
            if topbottom and leftright:
                print "BOOG"


            self.collision_react(sprite, topbottom, leftright, xoffset, yoffset)

        return colliding_sprites

    def collision_react(self, sprite, topbottom, leftright, xoffset, yoffset):
        # This is where collision reaction happen
        # It should be possible to change it
        if topbottom :
            self.entity.direction_y *= -1
            if yoffset > 0:
                self.entity.rect.bottom = sprite.rect.top - 1
            if yoffset < 0:
                self.entity.rect.top = sprite.rect.bottom + 1
        if leftright :
            self.entity.direction_x *= -1
            if xoffset > 0:
                self.entity.rect.right = sprite.rect.left - 1
            if xoffset < 0:
                self.entity.rect.left = sprite.rect.right + 1

class Attack(object):
    def __init__(self, game, entity):
        self.entity = entity
        self.game = game

    def attack(self, atk_x, atk_y):
        pass

class Fireball(Attack):
    """
    A bouncing fireball attack
    """
    def __init__(self, game, entity):
        self.entity = entity
        self.game = game

        self.movement = Movement(game, entity)
        self.movement.solid_sprites = game.current_level.blockers
        self.movement.solid_sprites += game.entities

    def attack(self, atk_x, atk_y):
        self.projectiles.append(
            Arrow2(self.game, self.entity,
                (self.entity.rect.centerx, self.entity.rect.centery),
                atk_x, atk_y,
                self.game.entities
            )
        )

    def update(self, dt, game):
        pass
