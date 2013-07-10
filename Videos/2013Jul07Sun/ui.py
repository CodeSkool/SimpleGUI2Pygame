import pygame, sys, pgxtra

class UI:
    jules_colors = {"light_blue":0xE5E6FFAA, "blue":0x0006AC55}
    def __init__(self, target, title="", width=640,
                 height=480, font=20,
                 bg_color=jules_colors["light_blue"],
                 fg_color=jules_colors["blue"]):
        """Initialize a UI object, and pygame."""
        self.target = target
        self.title = title
        self.width = width
        self.height = height
        self.font = font
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.controls = []
        self.transitioning = False

        pygame.init()
        self.clock = self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def start(self):
        """Set up the target and run the main game loop
        (handling events, drawing)."""
        # set up the target
        self.target.setup(self.screen)

        while True:
            if self.transitioning:
                # transition
                self.target = None
                return

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

    def transition(self):
        self.transitioning = True

    def handle_events(self):
        """Check for events and allow them to be handled."""
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
        """Allow everything to draw itself."""
        for control in self.controls:
            control.draw()
        self.target.update(self.screen)

    def quit(self):
        """Notify the target that we are quiting, then quit."""
        try:
            self.target.quit()
        finally:
            # always quit, even if there are exceptions
            quit()

    def draw_text(self, screen, text, location=None, font_size=None, align=-1):
        """Draw the specified text to the screen at the specified location.
        Return the text surface.
        """
        assert align >= -1 and align <= 1, "align must be -1, 0, or 1"
        if location == None:
            location = (10, 10)
        if font_size == None:
            font_size = self.font
        if pygame.font:
            font = pygame.font.Font("Comfortaa-Regular.ttf", font_size)
            text = font.render(text, 1, pygame.Color(self.fg_color))
            textpos = text.get_rect()

            if align == -1:
                textpos.x, textpos.y = location[0], location[1]
            elif align == 0:
                textpos.centerx, textpos.centery = location[0], location[1]
            else:
                textpos.right, textpos.y = location[0], location[1]

            screen.blit(text, textpos)
            return text

    def add_label(self, screen, text, location=None):
        """Draw a label (same as draw_text).
        """
        return self.draw_text(screen, text, location)

    def add_input(self, screen, text, handler, location=None, size=None, font_size=None, len_cap=0):
        """Add a new InputField to the UI."""
        if location == None:
            location = (10, 10)
        if size == None:
            size = (100, 25)
        if font_size == None:
            font_size = self.font
        textinput = pgxtra.InputField(screen, text, self.bg_color, self.fg_color, location, size, handler, font_size=font_size, len_cap=len_cap)
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

    def draw_circle(self, screen, color=None, pos=None, radius=10, width=0):
        if color == None:
            color = self.fg_color
            color = UI.jules_colors["blue"]
        if pos == None:
            pos = (radius, radius)
        return pygame.draw.circle(screen, color, pos, radius, width)

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
