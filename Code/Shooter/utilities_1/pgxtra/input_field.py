import pygame
from pgxtra import LEGAL_KEYS
from pgxtra_widget import PgxtraWidget


class InputField(PgxtraWidget):
    ''' Creates an input field on a solid colored rectangular background.
        Attributes:
            label = string of text on widget
            text_color = rgb color value of label text
            bg_color = rgb color value of widget background
            position = top left corner of widget
            fld_size = size of input field
            func_call = function that will handle widget event
            font_size = default set to 40
            len_cap = default set to 0, character cap on label
            focus = sets keyboard focus to this widget, default is False
                (Can only type in an input field with focus, and only one
                input field should have focus at any given time. If 2 or more
                fields have True focus at the same time, any typing will occur
                in both, and any return presses will call both fields'
                function calls. As long as only 1 or fewer fields is set to
                True, the class method check_event will handle updating all
                fields as necessary.)

        Widget label text will be centered and gray on the widget initially.
        If widget is enabled, upon left button press, field will erase and
        focus will become True, if not already. Text color will become value
        passed when initialized. When return is pressed, contents of field are
        passed to function call and focus is removed. Focus can be re-
        established by clicking the field again. To avoid this, call disable()
        on the widget.

        self.enabled = True if the widget is active, default is True
        '''

    def __init__(self, label, text_color, bg_color, position,
                 fld_size, func_call, font_size=40, len_cap=0, focus=False):
        PgxtraWidget.__init__(self)
        self.label = label
        self.default_label = self.label[:]
        self.text_color = text_color
        self.bg_color = bg_color
        self.pos = position
        self.size = fld_size
        self.func_call = func_call
        self.font_size = font_size
        self.len_cap = len_cap
        self.rect = pygame.Rect(self.pos, self.size)
        self.cursor = '|'
        self.blink_rate = 500
        self.focused = focus

        self.render_text(self.label)

    def render_text(self, rend_text):
        font = pygame.font.Font(None, self.font_size)
        if self.default_label in rend_text:
            text = font.render(rend_text, 1, pygame.Color('gray'))
        else:
            text = font.render(rend_text, 1, self.text_color)
        size = font.size(self.label)
        textpos = ((self.size[0] - size[0]) // 2 + self.pos[0],
                   (self.size[1] - size[1]) // 2 + self.pos[1])
        self.text = text
        self.textpos = textpos

    def draw(self, screen):
        if self.focused:
            time = pygame.time.get_ticks()
            if time % (self.blink_rate * 2) < self.blink_rate:
                self.cursor = " "
            else:
                self.cursor = "|"
        else:
            self.cursor = ""

        text = self.label + self.cursor
        self.render_text(text)
        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.text, self.textpos)

    def is_active(self):
        return self.enabled

    def mouse_release(self):
        if self.enabled and self.pressed:
            self.bg_color, self.text_color = self.text_color, self.bg_color
            self.pressed = False

    def mouse_press(self):
        if self.enabled:
            self.bg_color, self.text_color = self.text_color, self.bg_color
            self.pressed = True
            self.change_label("")

    def mouse_hover(self, hover):
        if hover:
            self.hover = True
        if not hover:
            self.hover = False

    def get_surface_rect(self):
        return self.rect

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

    def call(self):
        self.func_call(self.label)

    def set_focus(self):
        self.focused = True

    def remove_focus(self):
        self.focused = False

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
                if surface_rect != None and surface_rect.collidepoint(pos):
                    self.mouse_press()
                    response = ""

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect != None and surface_rect.collidepoint(pos):
                    self.mouse_release()
                    if self.enable:
                        fields = self.pgutility().get_widgets(InputField)
                        for field in fields:
                            if field != self:
                                field.remove_focus()
                            else:
                                field.set_focus()

            if self.focused:
                label = self.get_label()
                default_label = self.get_default_label()
                response = label[:]
                if event.type == pygame.KEYDOWN:
                    if label == default_label:
                        self.change_label('')
                        response = self.label[:]

                    if event.key in LEGAL_KEYS:
                        response += LEGAL_KEYS[event.key]

                    elif event.key == pygame.K_BACKSPACE:
                        response = response[:-1]

                    elif event.key == pygame.K_RETURN:
                        self.call()
                        self.remove_focus()
                        #self.disable()

                    if label != response:
                        self.change_label(response)


def main():
    ## Basic tests
    pygame.init()
    w = InputField("Foo", None, None, (0, 0), (10, 10), lambda: None)
    print w

if __name__ == '__main__':
    main()
