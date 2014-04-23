import pygame

import resources

class SoundFx(object):

    def __init__(self, name):
        self.enabled = pygame.mixer.get_init() is not None
        self.sounds = {
            'hit':pygame.mixer.Sound(resources.getValue('%s.hitsound' % (name))),
        }

    def play_sound(self, sound):
        sound = self.sounds.get(sound, None)
        if sound:
            # chan = pygame.mixer.find_channel()
            # if chan :
            #     chan.play(sound)
            sound.stop()
            sound.play()
