#!/usr/local/bin/python

import pygame, pygame.locals


class TimerEvents:
    SplashScreen = pygame.USEREVENT + 1
    GameOver = pygame.USEREVENT + 2

    def start(self, eventid, milliseconds=1000):
        pygame.time.set_timer(eventid, int(milliseconds))

    def stop(self, eventid):
        pygame.time.set_timer(eventid, 0)

def main():
    # basic testing
    pygame.init()
    t = TimerEvents()
    t.start(TimerEvents.SplashScreen, 500)
    t.stop(TimerEvents.SplashScreen)
    print "Started and stopped timer"

if __name__ == '__main__':
    main()
