__author__ = 'benoit'

import pygame
import resources

class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load(resources.getImage('player'))
        self.rect = pygame.rect.Rect(resources.getValue('player.start'), self.image.get_size())
        self.h_speed = resources.getValue('player.speed')
        self.v_speed = resources.getValue('player.speed')

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.x -= self.h_speed * dt
        if key[pygame.K_RIGHT]:
            self.rect.x += self.h_speed * dt
        if key[pygame.K_UP]:
            self.rect.y -= self.v_speed * dt
        if key[pygame.K_DOWN]:
            self.rect.y += self.h_speed * dt

        for cell in pygame.sprite.spritecollide(self, game.walls, False):
            self.rect = last

