#!/usr/local/bin/python

import pygame
from utilities_1 import state, basesprite


class TestingState(state.State):
    def __init__(self):
        state.State.__init__(self)
        pass

    def setup(self):
        filename = "resources\\breakout_block_fading.png"
        width, height, columns = 64, 32, 18
        sprite = basesprite.BaseSprite(filename, width, height, columns, True)
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(sprite)

    def update(self, screen):
        self.sprite_group.update()
        self.sprite_group.draw(screen)


if __name__ == "__main__":
    import doctest
    failed = 0
    result = doctest.testmod()
    print result
    if result[failed]:
        pass
    else:
        #pass
        TestingState().start()
