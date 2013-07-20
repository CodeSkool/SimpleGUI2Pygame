#!/usr/local/bin/python

import pygame

from utilities_1 import state as st
from utilities_1 import ui
from utilities_1 import pgxtra as pgx
from utilities_1 import imageloader as IL

import playing as pl
import timer_events as te
import high_scores as hs
from const import *

# Classes
class SplashScreen(st.State):
    def __init__(self, current=0):
        st.State.__init__(self)
        self.ui = ui.UI(self, Jules_UIContext)
        self.nextState = pl.Playing
        logo_duration = 3 * 1000
        start_duration = 8 * 1000
        scores_duration = 5 * 1000
        self.displays = [(logo_duration, self.draw_logo),
                         (start_duration, self.draw_start),
                         (scores_duration, self.draw_high_scores)]
        self.eventid = te.TimerEvents.SplashScreen
        self.current = current
        self.draw = self.displays[self.current][1]

        self.image = IL.ImageLoader("resources\\breakoutart.png")
        self.start_rect = pygame.Rect(0, 89, 158, 122)
        self.start_button_image = self.image.load(self.start_rect)
        self.start_button = None
        self.start_button_pos = (W/2 - 158/2, 7*H/10) # btn width (158, 61)

        self.pos = (0, 0)
        self.rect = pygame.Rect(self.pos, (W, H))
        self.logo = IL.ImageLoader("resources\\breakout_titlepg.png")
        self.logo_image = self.logo.load(self.rect)

        self.startpage = IL.ImageLoader("resources\\breakout_startpg.png")
        self.start_image = self.startpage.load(self.rect)

        self.hiscore = IL.ImageLoader("resources\\breakout_hspg.png")
        self.hiscore_image = self.hiscore.load(self.rect)

    def start(self):
        te.TimerEvents().start(eventid=self.eventid,
                            milliseconds=self.displays[self.current][0])
        st.State.start(self)

    def setup(self):
        self.start_button = pgx.SpecialButton(self.start_button_image,
                                          self.start_button_pos,
                                          (158, 61), (0, 0),
                                          lambda: self.transition(),
                                          press_offset=(0, 61))

    def handle(self, event):
        if event.type == self.eventid:
            self.increment_display()
            self.draw = self.displays[self.current][1]
            te.TimerEvents().start(eventid=self.eventid,
                                milliseconds=self.displays[self.current][0])
        elif self.current == 1:
            self.start_button.check_event(event)

    def quit(self):
        te.TimerEvents().stop(self.eventid)

    def increment_display(self):
        self.current += 1
        if self.current >= len(self.displays):
            self.current = 0

    def update(self, screen):
        self.draw(screen)

    def draw_high_scores(self, screen):
        screen.blit(self.hiscore_image, self.pos, self.rect)
        scores = hs.HighScores.high_scores
        spacing = 30
        dots = "".join([" ." * 15])
        for key, (name, score) in sorted(scores.items()):
            txt = "".join([name, dots, str(score)])
            self.ui.draw_text(txt, location=(W/2, H/2.5 + (key + 1) * H/12),
                              align=0)

    def draw_logo(self, screen):
        screen.blit(self.logo_image, self.pos, self.rect)


    def draw_start(self, screen):
        screen.blit(self.start_image, self.pos, self.rect)
        self.start_button.draw(screen)




def main():
    s = SplashScreen()
    s.start()
    ui.quit()

if __name__ == '__main__':
    main()
