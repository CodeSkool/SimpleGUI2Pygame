import pygame
from pgxtra_widget import PgxtraWidget

class Button(PgxtraWidget):
    '''Creates a button on a solid colored rectangular background.
        Attributes:
           label = string of text on widget
           text_color = rgb color value of label text
           bg_color = rgb color value of widget background
           position = top left corner of widget
           btn_size = size of button
           func_call = function that will handle widget event
           font_size = default set to 40
           len_cap = default set to 0, character cap on label

        Widget label text will be centered on the widget.
        If widget is enabled, upon left button press, colors of text & bg
        will reverse. Upon left button release, they will return to normal,
        and upon hovering, an outline box will appear.

        self.enabled = True if the widget is active, default is True
        '''

    def __init__(self, label, text_color, bg_color, position,
                 btn_size, func_call, font_size=40, len_cap=0):
        PgxtraWidget.__init__(self)
        self.label = label
        self.default_label = label
        self.text_color = text_color
        self.bg_color = bg_color
        self.orig_bg_color = bg_color
        self.pos = position
        self.size = btn_size
        self.func_call = func_call
        self.font_size = font_size
        self.len_cap = len_cap
        self.rect = pygame.Rect(self.pos, self.size)
        self.hover = False

        pos = self.pos[0] - 2, self.pos[1] - 2
        size = self.size[0] + 4, self.size[1] + 4
        self.outline_rect = pygame.Rect(pos, size)

        self.render_label()

    def render_label(self):
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.label, 1, self.text_color)
        text_press = font.render(self.label, 1, self.bg_color)
        size = font.size(self.label)
        textpos = ((self.size[0] - size[0]) // 2 + self.pos[0],
                   (self.size[1] - size[1]) // 2 + self.pos[1])
        self.text_norm = text
        self.text_press = text_press
        self.text = self.text_norm
        self.textpos = textpos

    def draw(self, screen):
        if self.hover:
            pygame.draw.rect(screen, self.bg_color, self.outline_rect, 1)
        else:
            pygame.draw.rect(screen, self.text_color, self.outline_rect, 1)

        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.text, self.textpos)

    def is_active(self):
        return self.enabled

    def mouse_release(self):
        if self.enabled and self.pressed and self.hover:
            self.bg_color, self.text = self.orig_bg_color, self.text_norm
            self.pressed = False
            self.func_call()

    def mouse_press(self):
        if self.enabled and self.hover:
            self.bg_color, self.text = self.text_color, self.text_press
            self.pressed = True

    def mouse_hover(self, hover):
        if hover:
            self.hover = True
        if not hover:
            self.hover = False
            self.bg_color, self.text = self.orig_bg_color, self.text_norm

    def get_surface_rect(self):
        return self.outline_rect

    def get_label(self):
        return self.label

    def get_default_label(self):
        return self.default_label

    def change_label(self, new_label):
        if self.len_cap:
            if len(new_label) <= self.len_cap:
                self.label = new_label
        else:
            self.label = new_label
        self.render_label()

    def call(self):
        self.func_call()

    def check_event(self, event):
        if self.is_active():
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect != None and surface_rect.collidepoint(pos):
                    self.mouse_hover(True)
                else:
                    self.mouse_hover(False)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.mouse_press()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.mouse_release()

def main():
    ## Basic tests
    pygame.init()
    w = Button("Foo", pygame.Color("blue"),
        pygame.Color("black"), (0,0), (10,10), lambda: None)
    print w

if __name__ == '__main__':
    main()