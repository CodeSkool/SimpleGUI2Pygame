#!/usr/local/bin/python

#-------------------------------------------------------------------------------
# Name:        React
# Author:      Jules
# Created:     07/08/2013
# Copyright:   (c) Julie Ann Stoltz 2013
# Licence:     DBAD (refer to http://www.dbad-license.org/)
#-------------------------------------------------------------------------------

import random
import itertools
import functools

import pygame, pygame.event, pygame.time

from filehelper import FileHelper
from state import State
from ui import UI, UIContext


# Screen resolution
W, H = 1280, 720

# Color objects
RED    = pygame.Color(255,  0,  0,255)
GREEN  = pygame.Color(  0,255,  0,255)
BLUE   = pygame.Color(  0,  0,255,255)
YELLOW = pygame.Color(255,255,  0,255)
LTBLUE = pygame.Color(178,223,238,255)
PURPLE = pygame.Color(255,  0,255,255)
LIME   = pygame.Color(  0,127,200,255)
VIOLET = pygame.Color(127,127,255,255)
PINK   = pygame.Color(200,  0,127,255)
BLACK  = pygame.Color(  0,  0,  0,255)
WHITE  = pygame.Color(255,255,255,255)
NAVY   = pygame.Color(  0,  0,128,255)

Jules_UIContext = UIContext("React", W, H, 0, "Comfortaa-Regular.ttf", 40,
                            BLACK, PINK, (0,0), (W/10, H/10), 0, 0, 0)

# Event IDs
class TimerEvents:
    SplashScreen = pygame.USEREVENT + 1
    GameStart = pygame.USEREVENT + 2
    Playing = pygame.USEREVENT + 3
    GameOver = pygame.USEREVENT + 4
    BuzzKill = pygame.USEREVENT + 5

    def start(self, eventid, milliseconds=1000):
        pygame.time.set_timer(eventid, int(milliseconds))

    def stop(self, eventid):
        pygame.time.set_timer(eventid, 0)


class HighScores:
    high_scores = None
    def __init__(self):
        self.high_scores_file = "React_HS.pkl"

    def load(self):
        HighScores.high_scores = FileHelper(self.high_scores_file).load()
        if HighScores.high_scores == None:
            keys = [i + 1 for i in range(10)]
            values = [("AAA", 100 * (i+1)) for i in range(10, 0, -1)]
            HighScores.high_scores = dict(itertools.izip(keys, values))

    def save(self):
        FileHelper(self.high_scores_file).save(HighScores.high_scores)


class SplashScreen(State):
    def __init__(self, current=0):
        State.__init__(self)
        self.ui = UI(self, Jules_UIContext)
        self.nextState = GameStart
        logo_duration = 20 * 1000
        scores_duration = 5 * 1000
        self.displays = [(logo_duration, self.draw_logo),
                        (scores_duration, self.draw_high_scores)]
        self.eventid = TimerEvents.SplashScreen
        self.current = current
        self.draw = self.displays[self.current][1]
        self.instructions = ['Can you think fast and react faster?',
                             'This game will test both.',
                             'Your job is to destroy the bonus blocks.',
                             'Sounds easy, right?... Wrong!',
                             'There are several problems.',
                             'If you destroy a penalty block you lose 200 pts.',
                             'If you get 3 penalties, you lose a life.',
                             'If you lose 3 lives, the game is over.',
                             'The bonus and penalty blocks',
                             'change colors every 5 seconds.',
                             'And on top of that, if you do not destroy a',
                             'random non-bonus, non-penalty block every',
                             'couple of seconds, that will give you a',
                             'penalty too. Think you got all that?']

    def start(self):
        TimerEvents().start(eventid=self.eventid,
                            milliseconds=self.displays[self.current][0])
        State.start(self)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            TimerEvents().stop(self.eventid)
            self.transition()
        elif event.type == self.eventid:
            self.increment_display()
            self.draw = self.displays[self.current][1]
            TimerEvents().start(eventid=self.eventid,
                                milliseconds=self.displays[self.current][0])

    def increment_display(self):
        self.current += 1
        if self.current >= len(self.displays):
            self.current = 0

    def update(self, screen):
        self.draw(screen)

    def draw_high_scores(self, screen):
        scores = HighScores.high_scores
        caption = "High Scores"
        self.ui.draw_text(screen, caption, location=(W/2, H/11), align=0)
        spacing = 30
        dots = "".join([" ." for i in range(spacing)])
        for key, (name, score) in sorted(scores.items()):
            txt = "".join([name, dots, str(score)])
            self.ui.draw_text(screen, txt,
                              location=(W/2, (key + 1) * H/12), align=0)

    def draw_logo(self, screen):
        logo = "React"
        prompt = "Click to begin"
        with self.ui.newcontext(UIContext(font_size=80, fg_color=PINK,
                                          bg_color=BLACK)):
            self.ui.draw_text(screen, logo, location=(W/2, H/6), align=0)
        self.ui.draw_text(screen, prompt, location=(W/2, H/4), align=0)

        with self.ui.newcontext(UIContext(font_size=26, fg_color=PINK,
                                          bg_color=BLACK)):
            i = 60
            for instruction in self.instructions:
                self.ui.draw_text(screen, instruction, location=(W/2, H/4 + i),
                                  align=0)
                i += 30


class GameStart(State):
    def __init__(self, lives=3, score=0):
        State.__init__(self)
        self.ui = UI(self, Jules_UIContext)
        self.lives = lives
        self.score = score
        self.nextState = lambda: Playing(self.lives, self.score)
        self.prompt = "Ready?"
        self.countdown_step = 500
        self.count = 3
        self.text = self.prompt
        self.eventid = TimerEvents.GameStart

    def start(self):
        self.start_timer()
        State.start(self)

    def handle(self, event):
        if event.type == self.eventid:
            self.text = str(self.count)
            if self.count == 0:
                self.text = "GO!"
                self.stop_timer()
                return
            self.count -= 1

    def start_timer(self):
        TimerEvents().start(eventid=self.eventid,
                            milliseconds=self.countdown_step)
    def stop_timer(self):
        TimerEvents().stop(eventid=self.eventid)
        self.transition()

    def update(self, screen):
        with self.ui.newcontext(UIContext(font_size=80, fg_color=PINK,
                                          bg_color=BLACK)):
            self.ui.draw_text(screen, self.text, location=(W/2, H/2), align=0)
        lives = "Lives: " + str(self.lives)
        score = "Score: " + str(self.score)
        self.ui.draw_text(screen, lives, location=(W/10, H/10), align=-1)
        self.ui.draw_text(screen, score, location=(9 * W/10, H/10), align=1)


class Playing(State):
    def __init__(self, lives=3, score=0, penalties=0):
        State.__init__(self)
        self.ui = UI(self, Jules_UIContext)
        self.nextState = None
        self.eventid = TimerEvents.Playing
        self.eventid2 = TimerEvents.BuzzKill
        self.score = score
        self.lives = lives
        self.penalties = penalties
        self.countdown = 5 * 1000
        self.penalties_per_life = 3
        self.start_time = pygame.time.get_ticks()
        self.squares = []
        self.bonus_color = self.rand_color()
        self.penalty_color = self.bonus_color
        while self.penalty_color == self.bonus_color:
            self.penalty_color = self.rand_color()
        self.limit = 2 * 1000

    def start(self):
        self.start_time = pygame.time.get_ticks()
        TimerEvents().start(eventid=self.eventid, milliseconds=self.countdown)
        TimerEvents().start(eventid=self.eventid2, milliseconds=self.limit)
        State.start(self)

    def handle(self, event):
        if event.type == self.eventid:
            self.bonus_color = self.rand_color()
            self.penalty_color = self.bonus_color
            while self.penalty_color == self.bonus_color:
                self.penalty_color = self.rand_color()
            self.start_time = pygame.time.get_ticks()
            TimerEvents().start(eventid=self.eventid,
                                milliseconds=self.countdown)

        elif event.type == self.eventid2:
            if self.penalties >= self.penalties_per_life - 1:
                if self.lives > 1:
                    self.nextState = lambda: GameStart(self.lives - 1,
                                                       self.score)
                else:
                    self.nextState = lambda: GameOver(self.score)
            else:
                self.nextState = lambda: Playing(self.lives, self.score,
                                                 self.penalties + 1)
            self.transition()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for square in self.squares:
                if square[3].collidepoint(event.pos):
                    self.destroy(square)
                    TimerEvents().start(eventid=self.eventid2,
                                        milliseconds=self.limit)
                    if square[2] == self.bonus_color:
                        self.score += 200
                    elif square[2] == self.penalty_color:
                        if self.penalties >= self.penalties_per_life - 1:
                            if self.lives > 1:
                                self.nextState = lambda: GameStart(
                                                        self.lives - 1,
                                                        self.score)
                            else:
                                self.nextState = lambda: GameOver(
                                                        self.score)
                        else:
                            self.nextState = lambda: Playing(self.lives,
                                                        self.score - 200,
                                                        self.penalties + 1)
                        self.transition()
                    else:
                        self.score += 25

    def setup(self, screen):
        for i in range(20):
            self.spawn()

    def rand_pos(self, side):
        xpos = random.randrange(side, W - side)
        ypos = random.randrange(2.5 * H/10 + side, H - side)
        pos = (xpos, ypos)
        rect = pygame.Rect(pos, (side, side))
        return pos, rect

    def is_unique(self, rect):
        if len(self.squares) == 0:
            return True
        for square in self.squares:
            if rect.colliderect(square[3]):
                return False
        return True

    def rand_color(self):
        return random.choice([RED, GREEN, BLUE, YELLOW, LTBLUE, PURPLE, LIME,
                              VIOLET, PINK, NAVY])

    def rand_vel(self):
        xvel = random.choice([-5,-4,-3,3,4,5])
        yvel = random.choice([-5,-4,-3,3,4,5])
        vel = (xvel, yvel)
        return vel

    def destroy(self, square):
        self.squares.remove(square)
        self.spawn()

    def spawn(self):
        side = 50
        pos, rect = self.rand_pos(side)
        while not self.is_unique(rect):
            pos, rect = self.rand_pos(side)
        color = self.rand_color()
        vel = self.rand_vel()
        self.squares.append([pos, (side, side), color, rect, vel])

    def get_time(self):
        return ((self.countdown - \
                (pygame.time.get_ticks() - self.start_time)) // 1000) + 1

    def update(self, screen):
        # draw stats
        time = "Next Change: " + str(self.get_time())
        lives = "Lives: " + str(self.lives)
        penalties = "Penalties: " + str(self.penalties) + " of " \
                    + str(self.penalties_per_life)
        score = "Score: " + str(self.score)
        self.ui.draw_text(screen, lives, location=(W/10, H/10), align=-1)
        self.ui.draw_text(screen, penalties, location=(W/10, 2*H/10), align=-1)
        self.ui.draw_text(screen, score, location=(9 * W/10, H/10), align=1)
        self.ui.draw_text(screen, time, location=(9 * W/10, 2 * H/10), align=1)
        self.ui.draw_text(screen, 'Bonus', (3*W/10+20, H/10 - 60), align=-1)
        self.ui.draw_text(screen, 'Penalty', (7*W/10-20, H/10 - 60), align=1)

        # update positions
        for square in self.squares:
            pos, vel = square[0], square[4]
            pos = (pos[0] + vel[0], pos[1] + vel[1])

            # if near edges or barrier, reverse direction
            side = square[1][0]
            if pos[0] < 0:
                pos = (0, pos[1])
                vel = (vel[0] * -1, vel[1])
            elif pos[0] > W - side:
                pos = (W - side, pos[1])
                vel = (vel[0] * -1, vel[1])

            if pos[1] < 2.5 * H/10 + side:
                pos = (pos[0], 2.5 * H/10 + side)
                vel = (vel[0], vel[1] * -1)
            elif pos[1] > H - side:
                pos = (pos[0], H - side)
                vel = (vel[0], vel[1] * -1)

            # update square data before going to next square
            square[0] = pos
            square[4] = vel
            rect = square[3]
            rect.topleft = pos
            square[3] = rect


        # draw squares
        screen.lock()
        try:
            for square in self.squares:
                pos = square[0]
                size = square[1]
                color = square[2]
                self.ui.draw_rect(screen, pos, size, color)
            self.ui.draw_rect(screen, (3*W/10+50, H/10 - 15), (60, 60),
                              self.bonus_color)
            self.ui.draw_rect(screen, (6*W/10+10, H/10 - 15), (60, 60),
                              self.penalty_color)
        finally:
            screen.unlock()


class GameOver(State):
    def __init__(self, score):
        State.__init__(self)
        self.ui = UI(self, Jules_UIContext)
        self.nextState = lambda: SplashScreen(current=1)
        self.eventid = TimerEvents.GameOver
        self.score = score
        self.countdown = 5 * 1000
        for key, (name, value) in sorted(HighScores.high_scores.items()):
            if score > value:
                self.replace = key
                break
        else:
            self.replace = None

    def start(self):
        if self.replace == None:
            TimerEvents().start(self.eventid, self.countdown)
        State.start(self)

    def handle(self, event):
        if event.type == self.eventid:
            self.transition()

    def transition(self):
        TimerEvents().stop(self.eventid)
        State.transition(self)

    def input_text(self, text):
        new_scores = {}
        text = text.upper()
        HS = HighScores.high_scores
        old_scores = sorted(HS.keys())
        index = old_scores.index(self.replace)
        for key in old_scores[:index]:
            new_scores[key] = HS[key]
        new_scores[self.replace] = (text, self.score)
        for index in xrange(index + 1, len(HS)):
            new_scores[old_scores[index]] = HS[old_scores[index - 1]]
        HS = new_scores
        high_scores.save()
        self.transition()

    def setup(self, screen):
        if self.replace == None:
            pass
        else:
            size = (75, 50)
            location = ((W/2) - (size[0] / 2), 6 * H/10)
            with self.ui.newcontext(UIContext(font_size=30, len_cap=3)):
                self.ui.add_input(screen, "___",
                                  lambda text: self.input_text(text),
                                  location=location, size=size)

    def update(self, screen):
        if self.replace == None:
            self.ui.draw_text(screen, "Game Over", (W/2, H/10), align=0)
            self.ui.draw_text(screen, "Your Score: " + str(self.score),
                              (W/2, 3 * H/10), align=0)
        else:
            self.ui.draw_text(screen, "Game Over", (W/2, H/10), align=0)
            self.ui.draw_text(screen, "New High Score!", (W/2, 3*H/10), align=0)
            self.ui.draw_text(screen, "Your Score: " + str(self.score),
                              (W/2, 4 * H/10), align=0)
            self.ui.draw_text(screen, "Enter your initials:", (W/2, 5 * H/10),
                              align=0)


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

if __name__ == '__main__':
    main()