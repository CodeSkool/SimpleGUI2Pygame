#!/usr/local/bin/python

#-------------------------------------------------------------------------------
# Name:        Breakout Revisited
# Purpose:     Another breakout game!!
# Author:      Jules
# Created:     07/17/2013
# Copyright:   (c) Julie Ann Stoltz 2013
# Licence:     DBAD (refer to http://www.dbad-license.org/)
#-------------------------------------------------------------------------------

import sys
import random
import math
import itertools
import functools

import pygame
from pygame.locals import *

from utilities_1 import state as st, pgxtra as pgx, filehelper as fh, ui
from utilities_1 import imageloader as IL, level_loader as LL
from utilities_1 import point, basesprite

from high_scores import HighScores
from timer_events import TimerEvents
from splash_screen import SplashScreen
from playing import Playing


# Classes
class Game:
    def __init__(self):
        global high_scores
        high_scores = HighScores()
        high_scores.load()

    def start(self, init_state):
        current_state = init_state()
        while current_state <> None:
            current_state.start()
            current_state = current_state.get_next_state()()


def main():
    Game().start(SplashScreen)
    #Game().start(lambda: GameOver(0))

if __name__ == '__main__':
    main()
