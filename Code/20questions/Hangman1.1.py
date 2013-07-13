#!/usr/local/bin/python

#-------------------------------------------------------------------------------
# Name:        Hangman 1.1
# Author:      Jules
# Created:     06/23/2013
# Copyright:   (c) Julie Ann Stoltz 2013
# Licence:     DBAD (refer to http://www.dbad-license.org/)
#-------------------------------------------------------------------------------

import random
import string
import sys
import pygame
import pgxtra

# Filename of word list
filename = 'techwords.txt'

W, H = 640, 480

class FileHelper:
    def open_file(self):
        """Tries to open a file in the specified mode. If the file does not
        exist, prints error msg to console & closes program.
       """
        try:
            the_file = open(filename, 'r')
        except IOError:
            print 'Dependent file missing:', filename
            pygame.quit()
            sys.exit()
        return the_file

    def load_words(self):
        """Load the words from a file if it exists."""
        file = self.open_file()
        words = file.read()
        global word_list
        word_list = words.split(',')
        file.close()


#-------------------------------------------------------------------------------
class UI:
    def __init__(self, target, title="", width=W,
                 height=H, font=40,
                 bg_color="black",
                 fg_color="lightblue"):
        self.target = target
        self.title = title
        self.width = width
        self.height = height
        self.font = font
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.buttons = []
        self.textinputs = []

        pygame.init()
        self.clock = self.fpsClock = pygame.time.Clock()

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.screen = pygame.Surface((self.width, self.height))

    def start(self):
        self.target.my_setup(self.screen)
        self.surface.blit(self.screen, (0,0))

        while True:
            self.screen.fill(pygame.Color(self.bg_color))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.quit()
                else:
                    for field in self.textinputs:
                        field.check_event(event)
                    for button in self.buttons:
                        button.check_event(event)

            for field in self.textinputs:
                field.draw()
            for button in self.buttons:
                button.draw()

            self.target.draw(self.screen)
            self.surface.blit(self.screen, (0,0))

            pygame.display.flip()

            #pygame.display.update()
            self.fpsClock.tick(30)

    def quit(self):
        self.target.quit()
        pygame.quit()
        sys.exit()

    def draw_text(self, screen, message, location):
        if pygame.font:
            font = pygame.font.Font(None, self.font)
            text = font.render(message, 1, pygame.Color(self.fg_color))
            textpos = text.get_rect()
            textpos.centerx = location[0]
            textpos.centery = location[1]
            screen.blit(text, textpos)

    def add_input(self, screen, text, handler, location=None, size=None):
        if location == None:
            location = (50, 50)
        if size == None:
            size = (200, 50)
        textinput = pgxtra.InputField(screen, text, self.bg_color,
                                      self.fg_color, location, size,
                                      handler, self.font)
        textinput.enabled = True
        textinput.draw()
        self.textinputs.append(textinput)
        return textinput

    def get_label(self, widget):
        if widget in self.textinputs:
            return widget.get_label()
        else:
            return None

    def add_label(self, screen, text, location=None):
        self.draw_text(screen, text, location)

    def add_button(self, screen, text, handler, location=None, size=None):
        if location == None:
            location = (50, 50)
        if size == None:
            size = (50, 50)
        button = pgxtra.Button(screen, text, self.bg_color, self.fg_color,
                               location, size, handler, self.font)
        button.enabled = True
        button.draw()
        self.buttons.append(button)


#-------------------------------------------------------------------------------
class State:
    def __init__(self):
        self.ui = UI(self, "Hangman")
        self.nextState = None

    def start(self):
        self.ui.start()

    def quit(self):
        pass

    def my_setup(self, frame):
        pass

    def draw(self, canvas):
        pass

    def get_next_state(self):
        return self.nextState

    def transition(self):
        next_state = self.get_next_state()
        if next_state <> None:
            switch_to = next_state()
            switch_to.start()


class GameStart(State):
    def __init__(self):
        State.__init__(self)
        self.nextState = Playing
        self.next_state_type = None
        self.message = "Let's play Hangman!"

    def play_again(self):
        self.transition()

    def load(self):
        FileHelper().load_words()
        self.transition()

    def my_setup(self, frame):
        self.ui.add_button(frame, "Click to Play", lambda btn: self.load(),
                           (W//2-100, H//2), (200, 60))

    def draw(self, canvas):
        self.ui.draw_text(canvas, self.message, (W//2, 100))


class Playing(State):
    def __init__(self, guess = None):
        State.__init__(self)
        self.next_state = self.get_next_state
        self.next_state_type = None
        self.word = ''
        self.guessed = []
        self.guesses = 10
        self.result = "You can only make 10 more guesses."
        self.guess = guess
        self.label = 'Type Here'

    def win(self):
        self.next_state_type = lambda: GameOver("You win!", self.word)
        self.transition()

    def lose(self):
        self.next_state_type = lambda: GameOver("You lose!", self.word)
        self.transition()

    def get_word(self):
        max_range = len(word_list)
        word_index = random.randrange(max_range)
        return word_list[word_index]

    def display_word(self):
        hint = ''
        for letter in self.word:
            if letter in self.guessed:
                hint += letter + ' '
            else:
                hint += '_ '
        return hint

    def display_left(self):
        msg = "You have " + str(self.guesses) + " guess(es) left."
        return msg

    def my_setup(self, frame):
        self.frame = frame
        self.word = self.get_word()
        self.get_input()

    def get_input(self):
        self.field = self.ui.add_input(self.frame, self.label,
                          lambda guess: self.get_guess(guess),
                          (W//2-100, H//2), (200, 60))

    def draw(self, canvas):
        self.ui.draw_text(canvas, self.display_left(), (W//2, 60))
        self.ui.draw_text(canvas, self.display_word(), (W//2, 140))
        self.ui.draw_text(canvas, 'Hit Enter when you have typed a letter',
                          (W//2, 0.8*H))
        self.ui.draw_text(canvas, self.result, (W//2, 0.7*H))

    def get_guess(self, guess):
        self.guess = guess
        self.field.change_label('')
        if self.guesses >= 1:
            valid = self.is_valid(self.guess)
            if valid:
                self.guessed.append(self.guess)
                word_letters = set(self.word)
                guess_letters = set(self.guessed)
                if self.guess in self.word and word_letters <= guess_letters:
                    self.win()
                    return
                elif self.guess in self.word:
                    self.result = guess.upper() + " was in the word."
                    #return #uncomment to make correct guesses not penalize
                else:
                    self.result = guess.upper() + " was not in the word."
                self.guesses -= 1
                if self.guesses <= 0:
                    self.lose()
                    return

    def is_valid(self, guess):
        if guess == None:
            return False
        elif guess.lower() not in 'abcdefghijklmnopqrstuvwxyz':
            self.result = "That is not a letter."
            return False
        elif guess.lower() in self.guessed:
            self.result = "You have already guessed that letter."
            return False
        return True

    def get_next_state(self):
        return self.next_state_type


class GameOver(State):
    def __init__(self, message, word):
        State.__init__(self)
        self.nextState = Playing
        self.next_state_type = None
        self.message = message
        self.word = word
        str = 'The word was ' + word + '.'
        self.answer = str

    def play(self):
        self.transition()

    def my_setup(self, frame):
        self.ui.add_button(frame, "Play Again", lambda btn: self.play(),
                           (W//2-250, H//2), (200, 60))
        self.ui.add_button(frame, "Quit", lambda btn: self.ui.quit(),
                           (W//2+50, H//2), (200, 60))

    def draw(self, canvas):
        self.ui.draw_text(canvas, self.message, (W//2, 75))
        self.ui.draw_text(canvas, self.answer, (W//2, 125))


#-------------------------------------------------------------------------------
def main():
    game = GameStart()
    game.start()

if __name__ == '__main__':
    main()