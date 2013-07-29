import sys
import contextlib
import pygame

from utilities_1 import pgxtra
from ui_context import UIContext


class UI:
    default_context = UIContext()

    def __init__(self, target, context=None):
        """Initialize a UI object."""
        self.target = target
        self.context = input_or_default(UI.default_context, context)
        self.controls = []
        self.transitioning = False
        pygame.init()
        self.clock = self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.context.width,
                                               self.context.height))
        pygame.display.set_caption(self.context.title)

    def start(self):
        """Set up the target and run the main game loop (handling events,
        drawing)."""

        # set up the target
        self.target.setup()

        while True:
            if self.transitioning:
                # transition
                self.target = None
                return

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

    def get_sounds(self, filename):
        sound = pygame.mixer.Sound(filename)
        return sound

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
        self.target.update(self.screen)
        for control in self.controls:
            control.draw(self.screen)

    def quit(self):
        """Notify the target that we are quiting, then quit."""
        try:
            self.target.quit()
        finally:
            # always quit, even if there are exceptions
            quit_all()

    def draw_text(self, text, location=None, align=None):
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

            self.screen.blit(text, textpos)
            return text

    def add_label(self, text, location=None):
        """Draw a label (same as draw_text).
        """
        return self.draw_text(self.screen, text, location)

    def add_input(self, text, handler, location=None, size=None):
        """Add a new InputField to the UI."""
        location = input_or_default(self.context.location, location)
        size = input_or_default(self.context.size, size)

        textinput = pgxtra.InputField(text, self.context.bg_color,
                                      self.context.fg_color, location, size,
                                      handler, self.context.font_size,
                                      self.context.len_cap)
        textinput.enabled = True
        self.controls.append(textinput)
        return textinput

    def add_button(self, text, handler, location=None, size=None):
        """Add a new Button to the UI."""
        location = input_or_default(self.context.location, location)
        size = input_or_default(self.context.size, size)

        button = pgxtra.Button(text, self.context.bg_color,
                               self.context.fg_color, location, size, handler,
                               self.context.font_size)
        button.enabled = True
        self.controls.append(button)
        return button

    def draw_circle(self, location=None, radius=10):
        location = input_or_default(self.context.location, location)

        return pygame.draw.circle(self.screen, self.context.fg_color, location,
                                  radius, self.context.line_width)

    def draw_rect(self, location=None, size=None, color=None):
        location = input_or_default(self.context.location, location)
        size = input_or_default(self.context.size, size)
        color = input_or_default(self.context.fg_color, color)

        return pygame.draw.rect(self.screen, color, pygame.Rect(location,
                                                                size))

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


def input_or_default(default, input_value=None):
    if input_value == None:
        return default
    return input_value


def quit_all():
    """Stop Pygame and exit the program."""
    pygame.quit()
    sys.exit()
    

def main():
    pass


if __name__ == '__main__':
    main()
