import pygame

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
        self.location = input_or_default((0, 0), location)
        self.size = input_or_default((100, 25), size)

        # Alignment for objects, -1 = left, 0 = center, 1 = right
        self.align = input_or_default(-1, align)
        assert self.align == -1 or 0 or 1, "align must be -1, 0, or 1"

        # Length cap in number of characters, 0 = no cap
        self.len_cap = input_or_default(0, len_cap)

        # Outline width of drawn objects
        self.line_width = input_or_default(0, line_width)


def main():
    pass


if __name__ == '__main__':
    main()
