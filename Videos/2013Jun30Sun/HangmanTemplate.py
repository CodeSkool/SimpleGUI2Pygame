#!/usr/local/bin/python

# Hangman Template

import random
import string
import sys
import pygame
import pgxtra

# Filename of word list, this file needs to be in the same folder with this
# template. If it isn't, you will get an error.
filename = 'techwords.txt'


def open_file():
    """Tries to open a file in the specified mode. If the file does not
    exist, prints error msg to console & closes program.
   """
    try:
        the_file = open(filename, 'r')
    except IOError:
        print 'Dependent file missing:', file_name
        sys.exit()
    return the_file


def load_words():
    """Load the words from a file if it exists."""
    file = open_file()
    words = file.read()
    global word_list
    word_list = words.split(',')
    file.close()


def get_word():
    'returns random word (string) from word_list'


def display_word():
    'returns a string of the word with dashes substituted for unguessed letters'


def display_left():
    'returns a message (string) of how many guesses the player has left'


def is_valid():
    'verifies guess passes 3 requirements, returns false if not, true if so'


def get_guess():
    'processes players guess and returns result'


def main():
    pass # add code here to start you game, play through, and then end


if __name__ == '__main__':
    main()