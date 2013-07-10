import pygame, contextlib
def input_or_default(input=None, default):
    if input == None:
        return default
    return input

class UIContext:
    def __init__(self, color=None, size=None, location=None, line_width=None #etc
    ):
        self.color = input_or_default(color, "blue") # or whatever default
        self.size = input_or_default(size, (100, 100)) # or whatever default size
        # and so on

class UI:
    default_context = UIContext("black", (640, 480), (10,10), line_width=1)
    another_context = UIContext("pink") # contexts need not set every parameter

    def __init__(other_parameters, context=None):
        self.my_context = input_or_default(context, UI.default_context)
    #...

    # example of usage
    def draw_something(screen=None, pos, radius):
        screen = input_or_default(screen, self.screen)
        pygame.draw.circle(screen, color=self.my_context.color, pos=pos,
                            radius=radius, width=self.my_context.line_width)

    # this next part will let us use the "with" keyword
    @contextlib.contextmanager
    def newcontext(self, context=None):
        context = input_or_default(context, self.my_context)
        # save the current context
        oldcontext = self.my_context
        # and apply the new context
        self.my_context = context
        try:
            # do whatever is wrapped in the "with" block
            yield
        finally:
            # restore the old context
            self.my_context = oldcontext


class SomeStateClass:

    def __init__(self):
        self.ui = UI()

    def update(self, screen):
        # viola! we can wrap UI calls with whatever context we like!
        with self.ui.newcontext(UI.another_context):
            self.ui.draw_something(screen, (1,1), 10)

        # can create new contexts on the fly too (don't need to store them)
        with self.ui.newcontext(UIContext("red")):
            self.ui.draw_something(screen, (200,200), 30)