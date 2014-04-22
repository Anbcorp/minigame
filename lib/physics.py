import pygame

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

class BaseDisplacement(Displacement):
    """
    Handle basic moving of objects with simple collision handling

    Objects will be blocked by anything in colliding_sprites
    """
    def __init__(self, entity):
        super(BaseDisplacement, self).__init__(entity)


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

class ReboundDisplacement(BaseDisplacement):
    """
    Anything we collide with will produce a (more or less) realistic rebound
    """

    def collision_react(self, sprite, topbottom, leftright, xoffset, yoffset):
        """
        Handles rebound when colliding into something
        """
        if topbottom :
            self.entity.vector[1] *= -1
            if yoffset > 0:
                self.entity.rect.bottom = sprite.rect.top - 1
            if yoffset < 0:
                self.entity.rect.top = sprite.rect.bottom + 1
        if leftright :
            self.entity.vector[0] *= -1
            if xoffset > 0:
                self.entity.rect.right = sprite.rect.left - 1
            if xoffset < 0:
                self.entity.rect.left = sprite.rect.right + 1

