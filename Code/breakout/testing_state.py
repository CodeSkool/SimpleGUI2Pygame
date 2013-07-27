#!/usr/local/bin/python

from utilities_1 import state


class TestingState(state.State):
    def __init__(self):
        state.State.__init__(self)
        pass


if __name__ == "__main__":
    TestingState().start()
