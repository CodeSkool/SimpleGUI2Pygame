import pygame, threading
from pgxtra_utility import PGxtraUtility

class PgxtraWidget(pygame.sprite.Sprite):
    _pgutility = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.enabled = True
        pygame.mouse.set_visible(True)
        # add widget to master list (do it in the base class)
        self.pgutility().add_widget(self)

    def pgutility(self):
        """The _pgutility should be the same for all PgxtraWidget objects."""
        if PgxtraWidget._pgutility == None: # Check for None before locking
            with threading.Lock(): # Lock the thread while we create the helper
                if PgxtraWidget._pgutility == None: # Check for None again after locking
                    PgxtraWidget._pgutility = PGxtraUtility() # Create the helper
        return PgxtraWidget._pgutility

    def draw(self):
        pass

    def is_active(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def mouse_release(self):
        pass

    def mouse_press(self):
        pass

    def mouse_hover(self):
        pass

    def check_event(self, event):
        pass


def main():
    ## Basic tests
    pygame.init()
    w = PgxtraWidget()
    print w

if __name__ == '__main__':
    main()
