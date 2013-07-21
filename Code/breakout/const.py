#!/usr/local/bin/python

import pygame
from utilities_1 import level_loader as LL
from utilities_1 import ui

# CONSTANTS

W, H = 800, 700 ## Screen width and height

LEVELS = LL.LevelLoader("resources\\levels.txt").open_file()

DK_PURPLE = pygame.Color(128,  0,255,255)
BLACK  = pygame.Color(  0,  0,  0,255)

Jules_UIContext = ui.UIContext("Breakout Revisited", W, H, 0,
                            "resources\\Comfortaa-Regular.ttf", 30,
                            BLACK, DK_PURPLE, (0,0), (W/10, H/10), 0, 0, 0)

REBOUND_SOUND_FILES = { "boop1" : "resources\\boop1.ogg",
                "beep1" : "resources\\beep1.ogg",
                "bop1" : "resources\\bop1.ogg",
                }

def main():
    print (W, H)
    print LEVELS
    print DK_PURPLE, BLACK
    print Jules_UIContext
    print REBOUND_SOUND_FILES

if __name__ == '__main__':
    main()
