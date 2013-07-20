#!/usr/local/bin/python

##
import pygame
##
from utilities_1 import state as st
from utilities_1 import ui
from utilities_1 import imageloader as IL

import high_scores as hs
import timer_events as te
import splash_screen as ss
from const import *

# Constants


# Classes
class GameOver(st.State):
    def __init__(self, score):
        st.State.__init__(self)
        self.ui = ui.UI(self, Jules_UIContext)
        self.nextState = lambda: ss.SplashScreen(current=1)
        self.eventid = te.TimerEvents.GameOver
        self.score = score
        self.countdown = 5 * 1000
        for key, (name, value) in sorted(hs.HighScores.high_scores.items()):
            if self.score > value:
                self.replace = key
                break
        else:
            self.replace = None

    def start(self):
        if self.replace == None:
            te.TimerEvents().start(self.eventid, self.countdown)
        st.State.start(self)

    def handle(self, event):
        if event.type == self.eventid:
            self.transition()

    def transition(self):
        te.TimerEvents().stop(self.eventid)
        st.State.transition(self)

    def input_text(self, text):
        new_scores = {}
        text = text.upper()
        old_scores = sorted(hs.HighScores.high_scores.keys())
        index = old_scores.index(self.replace)
        for key in old_scores[:index]:
            new_scores[key] = hs.HighScores.high_scores[key]
        new_scores[self.replace] = (text, self.score)
        for index in xrange(index + 1, len(hs.HighScores.high_scores)):
            new_scores[old_scores[index]] = hs.HighScores.high_scores[old_scores[index - 1]]
        hs.HighScores.high_scores = new_scores
        hs.HighScores().save()
        self.transition()

    def setup(self):
        self.pos = (0, 0)
        self.rect = pygame.Rect(self.pos, (W, H))
        self.gameover = IL.ImageLoader("resources\\breakout_endpg.png")
        self.gameover_image = self.gameover.load(self.rect)

        if self.replace == None:
            pass
        else:
            size = (75, 50)
            location = ((W/2) - (size[0] / 2), 8 * H/10 + 30)

            with self.ui.newcontext(ui.UIContext("Breakout Revisited", W, H, 0,
                                              "Comfortaa-Regular.ttf", 30,
                                              BLACK, DK_PURPLE, location, size,
                                              0, 3, 0)):
                self.ui.add_input("___", lambda text: self.input_text(text))

    def update(self, screen):
        screen.blit(self.gameover_image, self.pos, self.rect)
        if self.replace == None:
            self.ui.draw_text("Your Score: " + str(self.score),
                              (W/2, 6 * H/10), align=0)
        else:
            self.ui.draw_text("New High Score!", (W/2, 6*H/10), align=0)
            self.ui.draw_text("Your Score: " + str(self.score),
                              (W/2, 7 * H/10), align=0)
            self.ui.draw_text("Enter your initials:", (W/2, 8 * H/10),
                              align=0)



def main():
    hs.HighScores().load()
    g = GameOver(0)
    g.start()

    g = GameOver(100000)
    g.start()
    ui.quit()

if __name__ == '__main__':
    main()
