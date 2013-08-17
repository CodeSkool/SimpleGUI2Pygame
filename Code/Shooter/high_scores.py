#!/usr/local/bin/python

import itertools
from utilities_1 import filehelper as fh

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


def main():
    # basic test
    test_file = "test.pkl"
    h = HighScores()
    h.high_scores_file = test_file
    h.load()
    print HighScores.high_scores
    h.save()
    # cleanup
    import os
    os.remove(test_file)

if __name__ == '__main__':
    main()
