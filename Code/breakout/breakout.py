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

# CONSTANTS

W, H = 800, 700 ## Screen width and height

LEVELS = (
(7,7,7,7,7,7,7,7,7,7,7,7,
 7,2,5,0,5,7,7,5,0,5,2,7,
 7,2,5,0,5,7,7,5,0,5,2,7,
 7,2,5,0,5,7,7,5,0,5,2,7,
 7,2,2,2,2,2,2,2,2,2,2,7,
 7,2,2,2,2,2,2,2,2,2,2,7,
 7,2,5,0,5,7,7,5,0,5,2,7,
 7,2,5,0,5,7,7,5,0,5,2,7,
 7,2,5,0,5,7,7,5,0,5,2,7,
 7,7,7,7,7,7,7,7,7,7,7,7),

(3,3,3,3,3,3,3,3,3,3,3,3,
 3,6,6,6,6,6,6,6,6,6,6,3,
 3,6,3,3,3,3,3,3,3,3,6,3,
 3,6,3,6,6,6,6,6,6,3,6,3,
 3,6,3,6,3,3,3,3,6,3,6,3,
 3,6,3,6,3,3,6,3,6,3,6,3,
 3,6,3,6,6,6,6,3,6,3,6,3,
 3,6,3,3,3,3,3,3,6,3,6,3,
 3,6,6,6,6,6,6,6,6,3,6,3,
 3,3,3,3,3,3,3,3,3,3,6,3),

(6,6,6,2,2,2,4,4,4,7,7,7,
 2,2,2,4,4,4,7,7,7,6,6,6,
 4,4,4,7,7,7,6,6,6,2,2,2,
 7,7,7,6,6,6,2,2,2,4,4,4,
 6,6,6,2,2,2,4,4,4,7,7,7,
 2,2,2,4,4,4,7,7,7,6,6,6,
 4,4,4,7,7,7,6,6,6,2,2,2,
 7,7,7,6,6,6,2,2,2,4,4,4,
 6,6,6,2,2,2,4,4,4,7,7,7,
 2,2,2,4,4,4,7,7,7,6,6,6),

(6,6,6,6,6,6,6,6,6,6,6,6,
 7,8,0,0,0,8,8,0,0,0,8,7,
 7,8,7,7,7,8,8,7,7,7,8,7,
 7,8,0,0,0,8,8,0,0,0,8,7,
 7,8,8,8,8,8,8,8,8,8,8,7,
 7,8,8,8,8,8,8,8,8,8,8,7,
 7,8,0,0,0,8,8,0,0,0,8,7,
 7,8,7,7,7,8,8,7,7,7,8,7,
 7,8,0,0,0,8,8,0,0,0,8,7,
 6,6,6,6,6,6,6,6,6,6,6,6),

(1,1,1,1,1,1,1,1,1,1,1,1,
 1,3,1,1,1,3,3,1,1,1,3,1,
 1,3,1,0,1,3,3,1,0,1,3,1,
 1,3,1,1,1,3,3,1,1,1,3,1,
 1,1,3,3,3,1,1,3,3,3,1,1,
 1,1,3,3,3,1,1,3,3,3,1,1,
 1,3,1,1,1,3,3,1,1,1,3,1,
 1,3,1,0,1,3,3,1,0,1,3,1,
 1,3,1,1,1,3,3,1,1,1,3,1,
 1,1,1,1,1,1,1,1,1,1,1,1),

(5,5,5,5,5,5,5,5,5,5,5,5,
 5,5,5,5,5,5,5,5,5,5,5,5,
 4,4,4,4,4,4,4,4,4,4,4,4,
 4,4,4,4,4,4,4,4,4,4,4,4,
 3,3,3,3,3,3,3,3,3,3,3,3,
 3,3,3,3,3,3,3,3,3,3,3,3,
 2,2,2,2,2,2,2,2,2,2,2,2,
 2,2,2,2,2,2,2,2,2,2,2,2,
 1,1,1,1,1,1,1,1,1,1,1,1,
 1,1,1,1,1,1,1,1,1,1,1,1),

(5,5,5,5,5,5,5,5,5,5,5,5,
 5,5,5,5,5,5,5,5,5,5,5,5,
 4,4,0,0,4,4,4,4,0,0,4,4,
 4,4,4,4,4,4,4,4,4,4,4,4,
 3,3,3,3,3,0,0,3,3,3,3,3,
 3,3,3,3,3,0,0,3,3,3,3,3,
 2,2,2,2,2,2,2,2,2,2,2,2,
 2,2,0,0,2,2,2,2,0,0,2,2,
 1,1,1,1,1,1,1,1,1,1,1,1,
 1,1,1,1,1,1,1,1,1,1,1,1),

(2,2,2,2,2,2,2,2,2,2,2,2,
 2,0,0,0,2,2,2,2,0,0,0,2,
 2,0,0,0,2,2,2,2,0,0,0,2,
 2,2,2,2,5,5,5,5,2,2,2,2,
 2,2,2,2,5,5,5,5,2,2,2,2,
 2,2,2,2,5,5,5,5,2,2,2,2,
 2,2,2,2,5,5,5,5,2,2,2,2,
 2,0,0,0,2,2,2,2,0,0,0,2,
 2,0,0,0,2,2,2,2,0,0,0,2,
 2,2,2,2,2,2,2,2,2,2,2,2),

(1,1,1,1,1,1,1,1,1,1,1,1,
 1,3,0,0,0,3,3,0,0,0,3,1,
 1,3,0,0,0,3,3,0,0,0,3,1,
 1,3,0,0,0,3,3,0,0,0,3,1,
 1,3,3,3,3,3,3,3,3,3,3,1,
 1,3,3,3,3,3,3,3,3,3,3,1,
 1,3,0,0,0,3,3,0,0,0,3,1,
 1,3,0,0,0,3,3,0,0,0,3,1,
 1,3,0,0,0,3,3,0,0,0,3,1,
 1,1,1,1,1,1,1,1,1,1,1,1),

(3,6,8,2,2,0,0,2,2,8,6,3,
 6,8,2,2,0,2,2,0,2,2,8,6,
 8,2,2,0,2,2,2,2,0,2,2,8,
 2,2,0,2,2,8,8,2,2,0,2,2,
 2,0,2,2,8,6,6,8,2,2,0,2,
 0,2,2,8,6,3,3,6,8,2,2,0,
 2,2,8,6,3,3,3,3,6,8,2,2,
 2,8,6,3,3,0,0,3,3,6,8,2,
 8,6,3,3,0,2,2,0,3,3,6,8,
 6,3,3,0,2,2,2,2,0,3,3,6)

 )

DK_PURPLE = pygame.Color(128,  0,255,255)
BLACK  = pygame.Color(  0,  0,  0,255)

Jules_UIContext = ui.UIContext("Breakout Revisited", W, H, 0,
                            "resources\\Comfortaa-Regular.ttf", 30,
                            BLACK, DK_PURPLE, (0,0), (W/10, H/10), 0, 0, 0)


# Classes
class ImageLoader:
    '''Attempts to load image or any combination of sub-images.'''
    def __init__(self, filename):
        try:
            self.image = pygame.image.load(filename)
        except pygame.error, message:
            print 'Unable to load image:', filename
            #print message
            raise SystemExit

    # Load one sub-image from image given position as Rect object
    def load(self, rect):
        image = pygame.Surface(rect.size)
        image.blit(self.image, (0, 0), rect)
        return image

    # Load images given positions as Rects, return as list of images
    def load_list(self, rects):
        return [self.load(rect) for rect in rects]

    # Load a strip of images given position of first image as Rect object
    # (Note: The images have to be the same size.)
    def load_strip(self, rect, image_count):
        tuples = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                  for x in range(image_count)]
        return self.load_list(tuples)


class HighScores:
    high_scores = None
    def __init__(self):
        self.high_scores_file = "resources\\breakout_hs.pkl"

    def load(self):
        HighScores.high_scores = fh.FileHelper(self.high_scores_file).load()
        if HighScores.high_scores == None:
            keys = [i + 1 for i in range(5)]
            values = [("AAA", 100 * (i+1)) for i in range(5, 0, -1)]
            HighScores.high_scores = dict(itertools.izip(keys, values))

    def save(self):
        fh.FileHelper(self.high_scores_file).save(HighScores.high_scores)


class Point:
    '''Creates coordinate point with X and Y properties.'''
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self):
        return self.__x

    def setx(self, x):
        self.__x = x

    x = property(getx, setx)

    # Y property
    def gety(self):
        return self.__y

    def sety(self, y):
        self.__y = y

    y = property(gety, sety)


class BaseSprite(pygame.sprite.Sprite):
    '''Base class to create image objects that expands the pygame class.'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0,0.0)

    # X property
    def _getx(self):
        return self.rect.x

    def _setx(self,value):
        self.rect.x = value

    X = property(_getx,_setx)

    # Y property
    def _gety(self):
        return self.rect.y

    def _sety(self,value):
        self.rect.y = value

    Y = property(_gety,_sety)

    # position property
    def _getpos(self):
        return self.rect.topleft

    def _setpos(self,pos):
        self.rect.topleft = pos

    position = property(_getpos,_setpos)

    def set_image(self, image, width=0, height=0, columns=1):
        self.image = image
        if width == 0 and height == 0:
            self.frame_width = image.get_width()
            self.frame_width = image.get_height()
        else:
            self.frame_width = width
            self.frame_height = height
            rect = self.image.get_rect()
            self.last_frame = (rect.width//width) * (rect.height//height) - 1
        self.rect = Rect(0, 0, self.frame_width, self.frame_height)
        self.columns = columns

    def update(self, rate=30):
        # Handles animation if applicable
        current_time = pygame.time.get_ticks()
        if self.last_frame > self.first_frame:
            if current_time > self.last_time + rate:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_time = current_time
        else:
            self.frame = self.first_frame

        # Change image if necessary
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.image.subsurface(rect)
            self.old_frame = self.frame

class TimerEvents:
    SplashScreen = USEREVENT + 1
    GameOver = USEREVENT + 2

    def start(self, eventid, milliseconds=1000):
        pygame.time.set_timer(eventid, int(milliseconds))

    def stop(self, eventid):
        pygame.time.set_timer(eventid, 0)


class SplashScreen(st.State):
    def __init__(self, current=0):
        st.State.__init__(self)
        self.ui = ui.UI(self, Jules_UIContext)
        self.nextState = Playing
        logo_duration = 3 * 1000
        start_duration = 8 * 1000
        scores_duration = 5 * 1000
        self.displays = [(logo_duration, self.draw_logo),
                         (start_duration, self.draw_start),
                         (scores_duration, self.draw_high_scores)]
        self.eventid = TimerEvents.SplashScreen
        self.current = current
        self.draw = self.displays[self.current][1]

        self.image = ImageLoader("resources\\breakoutart.png")
        self.start_rect = pygame.Rect(0, 89, 158, 122)
        self.start_button_image = self.image.load(self.start_rect)
        self.start_button = None
        self.start_button_pos = (W/2 - 158/2, 7*H/10) # btn width (158, 61)

        self.pos = (0, 0)
        self.rect = pygame.Rect(self.pos, (W, H))
        self.logo = ImageLoader("resources\\breakout_titlepg.png")
        self.logo_image = self.logo.load(self.rect)

        self.startpage = ImageLoader("resources\\breakout_startpg.png")
        self.start_image = self.startpage.load(self.rect)

        self.hiscore = ImageLoader("resources\\breakout_hspg.png")
        self.hiscore_image = self.hiscore.load(self.rect)

    def start(self):
        TimerEvents().start(eventid=self.eventid,
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
            TimerEvents().start(eventid=self.eventid,
                                milliseconds=self.displays[self.current][0])
        elif self.current == 1:
            self.start_button.check_event(event)

    def quit(self):
        TimerEvents().stop(self.eventid)

    def increment_display(self):
        self.current += 1
        if self.current >= len(self.displays):
            self.current = 0

    def update(self, screen):
        self.draw(screen)

    def draw_high_scores(self, screen):
        screen.blit(self.hiscore_image, self.pos, self.rect)
        scores = HighScores.high_scores
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


class Playing(st.State):
    def __init__(self, lives=3, score=0, level=1, block_group=None):
        st.State.__init__(self)
        self.ui = ui.UI(self, Jules_UIContext)
        self.nextState = None
        self.score = score
        self.lives = lives
        self.level = level
        self.block_group = block_group
        self.waiting = True
        self.left_down = False
        self.right_down = False

    def start(self):
        st.State.start(self)

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_SPACE and self.waiting:
                self.waiting = False
                self.start_ball()

            elif event.key == K_LEFT:
                self.paddle.velocity.x = -10.0
                self.left_down = True

            elif event.key == K_RIGHT:
                self.paddle.velocity.x = 10.0
                self.right_down = True

        if event.type == KEYUP:
            if event.key == K_LEFT:
                self.left_down = False
                if self.right_down:
                    self.paddle.velocity.x = 10.0
                else:
                    self.paddle.velocity.x = 0

            elif event.key == K_RIGHT:
                self.right_down = False
                if self.left_down:
                    self.paddle.velocity.x = -10.0
                else:
                    self.paddle.velocity.x = 0

    def setup(self):
        # Load images
        self.image = ImageLoader("resources\\breakoutart.png")
        self.block_image = self.image.load(pygame.Rect(0, 0, 256, 64))
        self.brown_ball_image = self.image.load(pygame.Rect(234, 64, 16, 16))
        self.gray_ball_image = self.image.load(pygame.Rect(0, 64, 16, 16))
        self.short_paddle_image = self.image.load(pygame.Rect(16, 64, 88, 24))
        self.long_paddle_image = self.image.load(pygame.Rect(105, 64, 128, 24))

        # Create sprite groups
        self.paddle_group = pygame.sprite.Group()
        self.ball_group = pygame.sprite.Group()

        if self.block_group == None:
            self.block_group = pygame.sprite.Group()

            # Create blocks for level
            for bx in range(0, 12):
                for by in range(0, 10):
                    block = BaseSprite()
                    block.set_image(self.block_image, 64, 32, 4)
                    x = (W - 12 * 64)/2 + bx * (block.frame_width)
                    y = 32 * 2 + by * (block.frame_height)
                    block.position = x, y

                    # Read block from LEVELS
                    num = LEVELS[self.level-1][by * 12 + bx]
                    block.first_frame = num - 1
                    block.last_frame = num - 1
                    # Don't draw block for 0
                    if num > 0:
                        self.block_group.add(block)

        # Create paddle sprite
        self.paddle = BaseSprite()
        self.paddle.set_image(self.short_paddle_image, 88, 24, 1)
        self.paddle.position = W / 2, H - self.paddle.frame_height
        self.paddle_group.add(self.paddle)

        # Create ball sprite
        self.ball = BaseSprite()
        self.ball.set_image(self.gray_ball_image, 16, 16, 1)
        self.ball_group.add(self.ball)

    def update(self, screen):
        # Draw stats
        score = "Score: " + str(self.score)
        level = "Level: " + str(self.level)
        blocks = "Blocks: " + str(len(self.block_group))
        lives = "Lives: " + str(self.lives)

        self.ui.draw_text(score, location=(W/20, 10), align=-1)
        self.ui.draw_text(level, location=(6*W/20, 10), align=-1)
        self.ui.draw_text(blocks, location=(11*W/20, 10), align=-1)
        self.ui.draw_text(lives, location=(16*W/20, 10), align=-1)

        # Update blocks
        if len(self.block_group) == 0:
            if self.level < len(LEVELS) - 1:
                self.level += 1
                self.nextState = lambda: Playing(self.lives, self.score,
                                                 self.level)
                self.transition()
        self.block_group.update()

        # Move paddle
        self.paddle.X += self.paddle.velocity.x
        if self.paddle.X < 0:
            self.paddle.X = 0
        elif self.paddle.X > W - self.paddle.frame_width:
            self.paddle.X = W - self.paddle.frame_width

        # Move ball
        self.ball_group.update()
        if self.waiting:
            # Ball is resting on center of paddle
            self.ball.X = self.paddle.X + 36
            self.ball.Y = self.paddle.Y - 16

        # Update position of ball
        self.ball.X += self.ball.velocity.x
        self.ball.Y += self.ball.velocity.y

        if self.ball.X < 0:
            self.ball.X = 0
            self.ball.velocity.x *= -1
        elif self.ball.X > W - self.ball.frame_width:
            self.ball.X = W - self.ball.frame_width
            self.ball.velocity.x *= -1
        if self.ball.Y < 0:
            self.ball.Y = 0
            self.ball.velocity.y *= -1
        elif self.ball.Y > H - self.ball.frame_height:
            self.waiting = True
            self.lives -= 1
            self.nextState = lambda: Playing(self.lives, self.score, self.level,
                                             self.block_group)
            self.transition()
        if self.lives < 1:
            self.nextState = lambda: GameOver(self.score)
            self.transition()

        # Check for collision between ball and paddle
        if pygame.sprite.collide_rect(self.ball, self.paddle):
            self.ball.velocity.y = -abs(self.ball.velocity.y)
            bx = self.ball.X + 8
            by = self.ball.Y + 8
            px = self.paddle.X + self.paddle.frame_width/2
            py = self.paddle.Y + self.paddle.frame_height/2
            if bx < px:
                self.ball.velocity.x = -abs(self.ball.velocity.x)
            else:
                self.ball.velocity.x = abs(self.ball.velocity.x)

        # Check for collision between ball and blocks
        hit_block = pygame.sprite.spritecollideany(self.ball, self.block_group)
        if hit_block != None:
            self.score += 10
            self.block_group.remove(hit_block)
            bx = self.ball.X + 8
            by = self.ball.Y + 8

            # Above or below
            if bx > hit_block.X+5 and bx < hit_block.X + hit_block.frame_width-5:
                if by < hit_block.Y + hit_block.frame_height/2:
                    self.ball.velocity.y = -abs(self.ball.velocity.y)
                else:
                    self.ball.velocity.y = abs(self.ball.velocity.y)

            # left side
            elif bx < hit_block.X + 5:
                self.ball.velocity.x = -abs(self.ball.velocity.x)

            # Right side
            elif bx > hit_block.X + hit_block.frame_width - 5:
                self.ball.velocity.x = abs(self.ball.velocity.x)

            # Anything else
            else:
                self.ball.velocity.y *= -1

        # Draw everything
        self.block_group.draw(screen)
        self.ball_group.draw(screen)
        self.paddle_group.draw(screen)

    def start_ball(self):
        self.ball.velocity = Point(6.0, -8.0)


class GameOver(st.State):
    def __init__(self, score):
        st.State.__init__(self)
        self.ui = ui.UI(self, Jules_UIContext)
        self.nextState = lambda: SplashScreen(current=1)
        self.eventid = TimerEvents.GameOver
        self.score = score
        self.countdown = 5 * 1000
        for key, (name, value) in sorted(HighScores.high_scores.items()):
            if self.score > value:
                self.replace = key
                break
        else:
            self.replace = None

    def start(self):
        if self.replace == None:
            TimerEvents().start(self.eventid, self.countdown)
        st.State.start(self)

    def handle(self, event):
        if event.type == self.eventid:
            self.transition()

    def transition(self):
        TimerEvents().stop(self.eventid)
        st.State.transition(self)

    def input_text(self, text):
        new_scores = {}
        text = text.upper()
        old_scores = sorted(HighScores.high_scores.keys())
        index = old_scores.index(self.replace)
        for key in old_scores[:index]:
            new_scores[key] = HighScores.high_scores[key]
        new_scores[self.replace] = (text, self.score)
        for index in xrange(index + 1, len(HighScores.high_scores)):
            new_scores[old_scores[index]] = HighScores.high_scores[old_scores[index - 1]]
        HighScores.high_scores = new_scores
        high_scores.save()
        self.transition()

    def setup(self):
        self.pos = (0, 0)
        self.rect = pygame.Rect(self.pos, (W, H))
        self.gameover = ImageLoader("resources\\breakout_endpg.png")
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
    #Game().start(lambda: GameOver(605))

if __name__ == '__main__':
    main()
