import pygame



from lib.utils import *
from src import level
from src.entities import *

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
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                for listener in self.key_listeners:
                    listener.process_key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for listener in self.mouse_listeners:
                    listener.process_mouse_event(event)

class Game(object):

    # TODO: game is used everywhere, and we can't have multiple games instance
    # at the same time. Make it a singleton
    def __init__(self):
        self.event_listener = EventListener(self)
        self.running = True
        self.level = level.MazeLevel
        print 'Started game', id(self)

    def process_key_event(self, event):
        if event.key == pygame.K_n:
            print "New level"
            # TODO: should reset entities
            self.current_level = self.level()
            self.player.move(self.current_level.start_pos)
        if event.key == pygame.K_ESCAPE:
            self.quit()

    def quit(self):
        self.running = False

    def main(self, screen):
        clock = pygame.time.Clock()

        self.current_level = self.level()
        print "ok level"

        entities = level.ScrolledGroup()
        self.entities = entities
        self.player = Player(self, entities)
        self.player.move_to(self.current_level.start_pos)

        self.event_listener.register_listener(self, pygame.KEYDOWN)

        for i in range(0,100):
            ork = Enemy('ork', entities)
            # TODO: starting pos and proper collbox for enemies
            ork.rect = self.player.rect.copy()
            ork.rect.width = 16
            ork.rect.height = 16

        while self.running:
            dt = clock.tick(30)

            # process events
            self.event_listener.process_events()

            # update state of game
            entities.update(dt / 1000., self)
            self.current_level.update(dt / 1000., self)
           # tiles.update(dt / 1000., self)

            # draw screen
            screen.fill((255,0,0))
            self.current_level.draw(screen)
          #  tiles.draw(screen)
            entities.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.mixer.pre_init(buffer=2048)
    pygame.init()
    # TODO : screen size from conf ? Or at least constant
    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE|pygame.DOUBLEBUF)

    Game().main(screen)
