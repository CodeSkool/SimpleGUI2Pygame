import sys
import contextlib
import pygame
import pgxtra


NAVY = pygame.Color(0, 0, 128, 255)
LTBLUE = pygame.Color(178, 223, 238, 255)


def input_or_default(default, input_value=None):
    if input_value == None:
        return default
    return input_value


class UIContext:
    def __init__(self, title=None, width=None, height=None, display_flags=None,
                 font=None, font_size=None, bg_color=None, fg_color=None,
                 location=None, size=None, align=None, len_cap=None,
                 line_width=None):
        # Window title
        self.title = input_or_default("", title)

        # Screen resolution width & height
        self.width = input_or_default(640, width)
        self.height = input_or_default(480, height)

        # Flags to set display mode, 0 = standard windows mode with frame
        self.display_flags = input_or_default(0, display_flags)

        # Font type and size. TTF required for packaging as .exe
        self.font = input_or_default("Comfortaa-Regular.ttf", font)
        self.font_size = input_or_default(20, font_size)

        # Background and foreground pygame color objects
        self.bg_color = input_or_default(LTBLUE, bg_color)
        self.fg_color = input_or_default(NAVY, fg_color)

        # Location and size for objects
        self.location = input_or_default((0,0), location)
        self.size = input_or_default((100, 25), size)

        # Alignment for objects, -1 = left, 0 = center, 1 = right
        self.align = input_or_default(-1, align)
        assert self.align >= -1 and self.align <= 1, "align must be -1, 0, or 1"

        # Length cap in number of characters, 0 = no cap
        self.len_cap = input_or_default(0, len_cap)

        # Outline width of drawn objects
        self.line_width = input_or_default(0, line_width)


class UI:
    default_context = UIContext()

    def __init__(self, target, context=None):
        """Initialize a UI object."""
        self.target = target
        self.context = input_or_default(UI.default_context, context)
        self.controls = []

    def start(self):
        """Initialize pygame, set up the target and run the main game loop
        (handling events, drawing)."""
        pygame.init()
        self.clock = self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.context.width,
                                               self.context.height))
        pygame.display.set_caption(self.context.title)

        # set up the target
        self.target.setup(self.screen)

        while True:
            # fill the background color
            self.screen.fill(self.context.bg_color)
            # handle events
            self.handle_events()
            # draw things
            self.draw()

            # flip the display
            pygame.display.flip()
            # update the clock
            self.fpsClock.tick(30)


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

    def draw_text(self, screen, text, location=None, align=None):
        """Draw the specified text to the screen at the specified location.
        Return the text surface.
        """
        location = input_or_default(self.context.location, location)
        align = input_or_default(self.context.align, align)

        if pygame.font:
            font = pygame.font.Font(self.context.font,
                                    self.context.font_size)
            text = font.render(text, 1, self.context.fg_color)
            textpos = text.get_rect()

            if align == -1:
                textpos = location
            elif align == 0:
                textpos.center = location
            else:
                textpos.right, textpos.y = location[0], location[1]

            screen.blit(text, textpos)
            return text

    def add_label(self, screen, text, location=None):
        """Draw a label (same as draw_text).
        """
        return self.draw_text(screen, text, location)

    def add_input(self, screen, text, handler, location=None, size=None):
        """Add a new InputField to the UI."""
        location = input_or_default(self.context.location, location)
        size = input_or_default(self.context.size, size)

        textinput = pgxtra.InputField(screen, text,
                                      self.context.bg_color,
                                      self.context.fg_color,
                                      location, size, handler,
                                      self.context.font_size,
                                      self.context.len_cap)
        textinput.enabled = True
        self.controls.append(textinput)
        return textinput

    def add_button(self, screen, text, handler, location=None, size=None):
        """Add a new Button to the UI."""
        location = input_or_default(self.context.location, location)
        size = input_or_default(self.context.size, size)

        button = pgxtra.Button(screen, text, self.context.bg_color,
                               self.context.fg_color, location, size, handler,
                               self.context.font_size)
        button.enabled = True
        self.controls.append(button)
        return button

    def draw_circle(self, screen, location=None, radius=10):
        location = input_or_default(self.context.location, location)

        return pygame.draw.circle(screen, self.context.fg_color, location,
                                  radius, self.context.line_width)

    # this will allow the "with" keyword for context customization
    @contextlib.contextmanager
    def newcontext(self, context=None):
        context = input_or_default(self.context, context)
        # save the current context
        oldcontext = self.context
        # and apply the new context
        self.context = context
        try:
            # do whatever is wrapped in the "with" block
            yield
        finally:
            # restore the old context
            self.context = oldcontext


def quit():
    """Stop Pygame and exit the program."""
    pygame.quit()
    sys.exit()

def main():
    class tester:
        def __init__(self):
            self.ui = UI(self)
        def update(self, screen):
            self.ui.draw_text(screen,
                              "The quick brown fox jumps over the lazy dog.",
                              location=(10, 75))
        def setup(self, screen):
            self.ui.add_button(screen, "New button", self.button_handler)
            self.ui.add_input(screen, "New input", self.button_handler,
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

    quit()

if __name__ == '__main__':
   import doctest
   results = doctest.testmod()
   if results[0] == 0:
      main()
