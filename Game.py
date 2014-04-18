__author__ = 'Anb'

import pygame
import level

from entities import *

from utils import *

class EventListener(object):
    """
    Process pygame events, such as mouse or keyboard inputs
    """
    def __init__(self, game):
        self.key_listeners = set()
        self.mouse_listeners = set()
        self.game = game

    def register_listener(self, listener, event_type):
        if event_type == pygame.KEYDOWN:
            self.key_listeners.add(listener)
        if event_type == pygame.MOUSEBUTTONDOWN:
            self.mouse_listeners.add(listener)

    def process_events(self):
        events = [event for event in pygame.event.get()]

        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            if event.type == pygame.KEYDOWN:
                print "keydown"
                for listener in self.key_listeners:
                    listener.process_key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for listener in self.mouse_listeners:
                    listener.process_mouse_event(event)

class Game(object):

    def __init__(self):
        self.event_listener = EventListener(self)
        self.running = True

    def process_key_event(self, event):
        print "Game processing event"
        if event.key == pygame.K_n:
            print "New level"
            self.current_level = level.Level()
        if event.key == pygame.K_ESCAPE:
            self.quit()

    def quit(self):
        self.running = False

    def main(self, screen):
        clock = pygame.time.Clock()

        #tiles = level.ScrolledGroup()

        self.current_level = level.Level()
       # tiles.add(self.current_level.blockers)
       # tiles.add(self.current_level.tiles)

        entities = level.ScrolledGroup()
        self.entities = entities
        self.player = Player(entities)
        self.event_listener.register_listener(self.player, pygame.KEYDOWN)
        self.event_listener.register_listener(self, pygame.KEYDOWN)

        for i in range(0,1000):
            Anima(entities)
#        self.enemy = Ghosted(entities)

        while self.running:
            dt = clock.tick(30)


            # process events
            self.event_listener.process_events()

            # update state of game
            entities.update(dt / 1000., self)
            self.current_level.update(dt / 1000., self)
           # tiles.update(dt / 1000., self)

            # draw screen
            screen.fill(RED)
            self.current_level.draw(screen)
          #  tiles.draw(screen)
            entities.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    # TODO : screen size from conf ? Or at least constant
    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)

    Game().main(screen)
