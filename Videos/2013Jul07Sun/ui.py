import pygame, sys, pgxtra

class UI:
    def __init__(self, target, title="", width=640,
                 height=480, font=20,
                 bg_color="turquoise",
                 fg_color="violetred4"):
        """(UI, object, str, int, int, int, str, str) -> NoneType

        Initialize a UI object, and pygame."""
        self.target = target
        self.title = title
        self.width = width
        self.height = height
        self.font = font
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.controls = []

        pygame.init()
        self.clock = self.fpsClock = pygame.time.Clock()

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.screen = pygame.Surface((self.width, self.height))

    def start(self):
        """(UI) -> NoneType

        Set up the target and run the main game loop
        (handling events, drawing)."""
        # set up the target
        self.target.setup(self.screen)

        while True:
            # fill the background color
            self.screen.fill(pygame.Color(self.bg_color))
            # handle events
            self.handle_events()
            # draw things
            self.draw()

            # flip the display
            pygame.display.flip()
            # update the clock
            self.fpsClock.tick(30)


    def handle_events(self):
        """(UI) -> NoneType

        Check for events and allow them to be handled."""
        for event in pygame.event.get():
            # First, allow the target to handle the event
            self.target.handle(event)
            if event.type == pygame.QUIT:
                # handle the quit event
                self.quit()
            else:
                # allow controls to handle the event
                for control in self.controls:
                    control.check_event(event)

    def draw(self):
        """(UI) -> NoneType

        Allow everything to draw itself."""
        for control in self.controls:
            control.draw()
        self.target.update(self.screen)
        self.surface.blit(self.screen, (0,0))

    def quit(self):
        """(UI) -> NoneType

        Notify the target that we are quiting, then quit."""
        try:
            self.target.quit()
        finally:
            # always quit, even if there are exceptions
            quit()

    def draw_text(self, screen, text, location):
        """(UI, Surface, str, (int, int)) -> Surface
        Draw the specified text to the screen at the specified location.
        Return the text surface.
        """
        if pygame.font:
            font = pygame.font.Font(None, self.font)
            text = font.render(text, 1, pygame.Color(self.fg_color))
            textpos = text.get_rect()
            textpos.x = location[0]
            textpos.y = location[1]
            screen.blit(text, textpos)
            return text

    def add_label(self, screen, text, location=None):
        """(UI, surface, str, (int, int)) -> Surface
        Draw a label (same as draw_text).
        """
        return self.draw_text(screen, text, location)

    def add_input(self, screen, text, handler, location=None, size=None):
        """Add a new InputField to the UI."""
        if location == None:
            location = (10, 10)
        if size == None:
            size = (100, 25)
        textinput = pgxtra.InputField(screen, text, self.bg_color, self.fg_color, location, size, handler, self.font)
        textinput.enabled = True
        self.controls.append(textinput)
        return textinput


    def add_button(self, screen, text, handler, location=None, size=None):
        """Add a new Button to the UI."""
        if location == None:
            location = (10, 10)
        if size == None:
            size = (100, 25)
        button = pgxtra.Button(screen, text, self.bg_color, self.fg_color, location, size, handler, self.font)
        button.enabled = True
        self.controls.append(button)
        return button

def quit():
    """Stop Pygame and exit the program."""
    pygame.quit()
    sys.exit()


def main():
    class tester:
        def __init__(self):
            self.ui = UI(self, "Test Game")
        def update(self, screen):
            self.ui.draw_text(screen, "The quick brown fox jumps over the lazy dog.", location=(10, 75))
        def setup(self, screen):
            self.ui.add_button(screen, "New button", self.button_handler)
            self.ui.add_input(screen, "New input", self.button_handler, location=(10, 40))
        def handle(self, event):
            pass
        def button_handler(self, btn):
            pass
        def start(self):
            self.ui.start()
    try:
        tester().start()
        import time
        time.sleep(30)
    except Exception as e:
        print e
    finally:
        quit()

if __name__ == '__main__':
   import doctest
   results = doctest.testmod()
   if results[0] == 0:
      main()
