import sys
import contextlib
import pygame

from utilities_1 import pgxtra
from ui import UI, UIContext


def quit_all():
    """Stop Pygame and exit the program."""
    pygame.quit()
    sys.exit()


def main():
    class tester:
        def __init__(self):
            self.ui = UI(self)

        def update(self, screen):
            self.ui.draw_text("The quick brown fox jumps over the lazy dog.",
                              location=(10, 75))
            screen.lock()
            self.ui.draw_circle((50, 200), 30)
            self.ui.draw_rect((50, 300), (60, 60))
            screen.unlock()

        def setup(self):
            self.ui.add_button("New button", self.button_handler)
            self.ui.add_input("New input", self.button_handler,
                              location=(10, 40))

        def handle(self, event):
            pass

        def button_handler(self, btn):
            pass

        def start(self):
            self.ui.start()

    tester().start()
    import time
    time.sleep(30)

    quit_all()


if __name__ == '__main__':
    import doctest
    results = doctest.testmod()
    if results[0] == 0:
        main()
